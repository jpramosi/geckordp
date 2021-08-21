import re
import json
import configparser
import subprocess
import shutil
from time import sleep
from typing import List, Dict
from pathlib import Path
from geckordp.utils import wait_process_loaded, kill
from geckordp.firefox import Firefox
from geckordp.logger import log, dlog, elog, wlog, exlog
USER_PREF_REGEX = re.compile(r"\s*user_pref\(([\"'])(.+?)\1,\s*(.+?)\);")


class FirefoxProfile():
    """ An instance which represents the firefox profile.

        .. warning::
            Before making changes to a profile, it is recommend
            to clone the profile at first or creating a new one.
    """

    def __init__(self, name: str, is_relative: bool, path: Path):
        self.name = name
        self.is_relative = is_relative
        self.path = Path(path)
        self.__config_path = str(self.path.joinpath("prefs.js"))

    def list_config(self) -> List[Dict[str, str]]:
        """ Lists all configurations of the profile.

        Returns:
            List[Dict[str, str]]: A list with setting pairs.
        """
        # https://stackoverflow.com/questions/24548306/how-to-read-firefoxs-aboutconfig-entries-using-python
        entries = {}
        with open(self.__config_path) as f:
            lines = [line.rstrip() for line in f]
            for line in lines:
                m = USER_PREF_REGEX.match(line)
                if not m:
                    continue
                key, value = m.group(2), m.group(3)
                try:
                    entries[key] = json.loads(value)
                except Exception as ex:
                    elog(
                        f"failed to parse line '{line}' key:'{key}' value:'{value}' error:'{ex}'")
        return entries

    def set_required_configs(self):
        """ Sets all required settings to be able to use geckordp.
        """

        # disable crash-recover after 'ungraceful' process termination
        self.set_config("browser.sessionstore.resume_from_crash", False)
        # disable safe-mode after 'ungraceful' process termination
        self.set_config("browser.sessionstore.max_resumed_crashes", 0)
        self.set_config("toolkit.startup.max_resumed_crashes", -1)
        self.set_config("browser.sessionstore.restore_on_demand", False)
        self.set_config("browser.sessionstore.restore_tabs_lazily", False)
        # set download folder (not set by firefox)
        self.set_config("browser.download.dir", str(Path.home()))
        # enable compatibility
        self.set_config("devtools.chrome.enabled", True)
        self.set_config("devtools.cache.disabled", True)
        # don't open dialog to accept connections from client
        self.set_config("devtools.debugger.prompt-connection", False)
        # enable remote debugging
        self.set_config("devtools.debugger.remote-enabled", True)
        # allow tab isolation (for e.g. separate cookie-jar)
        self.set_config("privacy.userContext.enabled", True)
        # disable autoplay
        self.set_config("media.autoplay.blocking_policy", 2)
        self.set_config("media.autoplay.default", 5)
        # disable what's new
        self.set_config("browser.messaging-system.whatsNewPanel.enabled", False)
        self.set_config("browser.startup.homepage_override.mstone", "ignore")
        self.set_config("startup.homepage_override_url", "https://blank.org/")
        self.set_config("startup.homepage_welcome_url", "https://blank.org/")
        # misc
        self.set_config("devtools.theme", "dark")
        self.set_config("devtools.webconsole.timestampMessages", True)
        self.set_config("browser.aboutConfig.showWarning", False)
        self.set_config("browser.tabs.warnOnClose", False)
        self.set_config("browser.tabs.warnOnCloseOtherTabs", False)
        self.set_config(
            "browser.shell.skipDefaultBrowserCheckOnFirstRun", True)
        self.set_config("pdfjs.firstRun", True)
        self.set_config("doh-rollout.doneFirstRun", True)
        self.set_config("browser.startup.firstrunSkipsHomepage", True)
        self.set_config("browser.tabs.warnOnOpen", False)
        self.set_config("browser.warnOnQuit", False)
        self.set_config("toolkit.telemetry.reportingpolicy.firstRun", False)
        self.set_config("trailhead.firstrun.didSeeAboutWelcome", True)

    def set_config(self, name: str, value):
        """ Sets or updates a configuration value by its name.

        Args:
            name (str): The name of setting.
            value ([type]): The value of the setting.
        """
        input_lines = ""
        with open(self.__config_path, "r+") as f:
            input_lines = f.readlines()

        # make value json compatible
        if (isinstance(value, str)):
            value = f"\"{value}\""
        else:
            value = json.dumps(value)

        buffer = ""
        config_set = False
        for line in input_lines:
            m = USER_PREF_REGEX.match(line)
            if not m:
                continue
            key, val = m.group(2), m.group(3)
            try:
                if (not config_set and key == name):
                    line = f"user_pref(\"{name}\", {value});\n"
                    config_set = True
                buffer += line
            except Exception as ex:
                elog(
                    f"failed to parse line '{line}' key:'{key}' value:'{val}' error:'{ex}'")
                buffer += line

        if (not config_set):
            line = f"user_pref(\"{name}\", {value});\n"
            buffer += line

        with open(self.__config_path, "w") as f:
            f.write(buffer)

    def get_config(self, name):
        """ Get a configuration value by its name.

        Args:
            name ([type]): The name to retrieve the value from.

        Raises:
            JSONDecodeError: If value can not be deserialized.

        Returns:
            [type]: not None: The value of the setting, None: Setting not found
        """
        with open(self.__config_path, "r+") as f:
            input_lines = f.readlines()
            for line in input_lines:
                m = USER_PREF_REGEX.match(line)
                if not m:
                    continue
                key, val = m.group(2), m.group(3)
                if (key == name):
                    return json.loads(val, strict=False)
        return None

    def remove_config(self, name: str) -> bool:
        """ Removes a setting by its name.

        Args:
            name (str): The name of the setting to remove.

        Returns:
            bool: True: if setting found and removed, False: not found
        """
        input_lines = ""
        with open(self.__config_path, "r+") as f:
            input_lines = f.readlines()

        buffer = ""
        found = False
        for line in input_lines:
            m = USER_PREF_REGEX.match(line)
            if not m:
                continue
            key = m.group(2)
            if (not found and key == name):
                found = True
                continue
            buffer += line

        with open(self.__config_path, "w") as f:
            f.write(buffer)
        return found

    def __str__(self) -> str:
        return f"name:{self.name} is_relative:{self.is_relative} path:{str(self.path)}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, rhs):
        if (rhs is None):
            return False
        return self.name == rhs.name and self.path == rhs.path


class ProfileManager():
    """ A manager for firefox profiles.
        The manager allows to clone, add or remove firefox profiles.
        Each profile its configuration can be modified with 'FirefoxProfile'.

        .. warning::
            Before making changes to a profile, it is recommend
            to clone the profile at first or creating a new one.
    """

    def __init__(self, override_firefox_path="", override_profiles_path=""):
        # pylint: disable=invalid-name
        if (override_firefox_path == ""):
            override_firefox_path = Firefox.get_binary_path()
        self.__PROFILE = "remotefox_profile_manager"
        self.__ARGS = [override_firefox_path,
                       "-new-window",
                       "-new-instance",
                       "-no-remote",
                       "-no-default-browser-check"
                       ]

        if (override_profiles_path == ""):
            self.__profiles_path = Firefox.get_profiles_path()
        else:
            self.__profiles_path = Path(
                override_profiles_path).absolute()

        self.__profiles_ini = Path(
            self.__profiles_path).joinpath("profiles.ini")

        if (not self.__profiles_path.exists()):
            raise RuntimeError(
                f"path '{self.__profiles_path}' doesn't exist")

        if (not self.__profiles_ini.exists()):
            raise RuntimeError(
                f"'profiles.ini' doesn't exist in path '{self.__profiles_path}'")

        bk_profiles_ini = self.__profiles_ini.parent.joinpath(
            self.__profiles_ini.stem + "-bk" + self.__profiles_ini.suffix)
        
        if (not bk_profiles_ini.exists()):
            try:
                shutil.copyfile(self.__profiles_ini, bk_profiles_ini)
                log(f"backup file '{bk_profiles_ini}' created")
            except Exception as ex:
                exlog(f"copy backup file '{bk_profiles_ini}' failed:\n{ex}")

    def create(self, profile_name: str) -> FirefoxProfile:
        """ Creates and initializes a firefox profile with the specified name.

        Args:
            profile_name (str): The name for the new profile.

        Raises:
            RuntimeError: If initialization of profile failed.

        Returns:
            FirefoxProfile: not None: instance of firefox profile, None: initialization failed
        """
        if (self.exists(profile_name)):
            wlog(f"profile with name '{profile_name}' already exists")
            return None
        args = list(self.__ARGS)
        args.append("-CreateProfile")
        args.append(f"{profile_name}")
        subprocess.check_output(args, shell=False)        
        if (not self.__initialize_profile(profile_name)):
            raise RuntimeError(f"initialization of '{profile_name}' failed")

        profile = self.get_profile_by_name(profile_name)

        # need to sleep til no process is attached to the related files
        sleep(1)

        return profile

    def clone(self, source_name: str, dest_name: str, ignore_invalid_files=False) -> FirefoxProfile:
        """ Clones an existing firefox profile with the specified name.

        Args:
            source_name (str): The name of the profile to clone from.
            dest_name (str): The name of the new profile.

        Raises:
            ValueError: If 'source_name' and 'dest_name' are equal.
            ValueError: If 'source_name' is empty.
            ValueError: If 'dest_name' is empty.

        Returns:
            FirefoxProfile: not None: instance of firefox profile, None: source doesn't exists or destination already exists
        """
        if (source_name == dest_name):
            raise ValueError(
                f"parameter 'source_name' and 'dest_name' must be different")

        # check source profile
        if (source_name == ""):
            raise ValueError(f"parameter 'source_name' is empty")
        source_profile = self.get_profile_by_name(source_name)
        if (not source_profile):
            elog(f"profile with name '{source_name}' doesn't exist")
            return None
        if (not source_profile.path.exists()):
            elog(f"profile with path '{source_profile.path}' doesn't exist")
            return None

        # check destination profile
        if (dest_name == ""):
            raise ValueError(f"parameter 'dest_name' is empty")
        if (self.exists(dest_name)):
            elog(f"profile with name '{dest_name}' already exists")
            return None

        # create empty destination profile
        args = list(self.__ARGS)
        args.append("-CreateProfile")
        args.append(f"{dest_name}")
        subprocess.check_output(args, shell=False)

        dest_profile = self.get_profile_by_name(dest_name)
        if (not dest_profile):
            elog(f"profile with name '{dest_name}' doesn't exist")
            return None

        # copy contents
        log(f"copy from '{source_profile.path}' to '{dest_profile.path}'")
        if (dest_profile.path.exists()):
            shutil.rmtree(dest_profile.path)
        try:
            shutil.copytree(
                source_profile.path,
                dest_profile.path,
                ignore_dangling_symlinks=True,
                symlinks=True,
                ignore=shutil.ignore_patterns("times.json", "lock", "*.lock", "sessionstore.jsonlz4"))
        except shutil.Error as ex:
            if (not ignore_invalid_files):
                raise shutil.Error from ex
            else:
                wlog(f"copytree failed, some files could not be copied:\n{ex}")

        profile = self.get_profile_by_name(dest_name)

        # need to sleep til no process is attached to the related files
        sleep(1)

        return profile

    def remove(self, profile_name: str) -> bool:
        """ Removes a firefox profile by its name.

        Args:
            profile_name (str): The name of the profile to be removed.

        Raises:
            ValueError: If 'profile_name' is empty.
            ValueError: If 'profile_name' is 'default-release'.

        Returns:
            bool: True: profile found and removed, False: profile not found
        """
        if (profile_name == ""):
            raise ValueError(f"parameter 'profile_name' is empty")
        if (profile_name == "default-release"):
            raise ValueError(f"parameter 'profile_name' is 'default-release'")
        config = configparser.ConfigParser()
        config.optionxform = str  # preserve case

        found = False
        with open(str(self.__profiles_ini), "r") as f:
            config.read_file(f)
            sections = config.sections()
            for section in sections:
                name = config.get(section, "Name", fallback="")
                is_relative = int(config.get(
                    section, "IsRelative", fallback="1")) == 1
                path = config.get(section, "Path", fallback="")
                if (name != profile_name):
                    continue
                if (path == ""):
                    continue
                if (is_relative):
                    path = self.__profiles_path.joinpath(path)
                path = Path(path).absolute()
                if (not path.exists()):
                    continue
                log(f"remove path '{path}'")
                shutil.rmtree(path)
                log(f"remove section '{section}' with name '{name}'")
                config.remove_section(section)
                found = True
                break

        if (found):
            with open(str(self.__profiles_ini), "w+") as f:
                log(f"update profiles.ini")
                config.write(f, space_around_delimiters=False)
                return True

        return False

    def list_profiles(self) -> List[FirefoxProfile]:
        """ List all profiles available by firefox.

        Raises:

        Returns:
            List[FirefoxProfile]: List of firefox profiles.
        """
        profiles = []
        config = configparser.ConfigParser()
        with open(str(self.__profiles_ini), "r") as f:
            config.read_file(f)
            sections = config.sections()
            for section in sections:
                name = config.get(section, "Name", fallback="")
                is_relative = int(config.get(
                    section, "IsRelative", fallback="1")) == 1
                path = config.get(section, "Path", fallback="")
                if (is_relative):
                    path = self.__profiles_path.joinpath(path)
                profiles.append(
                    FirefoxProfile(name, is_relative, path))
        return profiles

    def exists(self, profile_name: str) -> bool:
        """ Check whether a profile exists.

        Args:
            profile_name (str): The profile name to check.

        Raises:

            ValueError: If 'profile_name' is empty.

        Returns:
            bool: True: profile exists, False: profile doesn't exists
        """
        if (profile_name == ""):
            raise ValueError(f"parameter 'profile_name' is empty")
        return self.get_profile_by_name(profile_name) is not None

    def get_profile_by_name(self, profile_name: str) -> FirefoxProfile:
        """ Get a profile by its name.

        Args:
            profile_name (str): The name of the profile to retrieve.

        Raises:
            ValueError: If 'profile_name' is empty

        Returns:
            FirefoxProfile: not None: instance of firefox profile, None: not found
        """
        if (profile_name == ""):
            raise ValueError(f"parameter 'profile_name' is empty")
        config = configparser.ConfigParser()
        with open(str(self.__profiles_ini), "r") as f:
            config.read_file(f)
            sections = config.sections()
            for section in sections:
                name = config.get(section, "Name", fallback="")
                is_relative = bool(config.get(
                    section, "IsRelative", fallback=True))
                path = config.get(section, "Path", fallback="")
                if (is_relative):
                    path = self.__profiles_path.joinpath(path)
                if (name == profile_name):
                    return FirefoxProfile(name, is_relative, path)
        return None

    def __initialize_profile(self, name: str) -> bool:
        # initialize a profile by starting firefox with the specified name
        args = list(self.__ARGS)
        args.append("-headless")
        args.append("-P")
        args.append(f"{name}")
        proc = subprocess.Popen(args, shell=False)
        dlog("wait for firefox to initialize profile")
        success = wait_process_loaded(proc.pid, timeout_sec=20.0)
        dlog("profile initialized")
        kill(proc)
        proc.wait(5.0)
        return success
