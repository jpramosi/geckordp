""" This basic example demonstrates how to list all tabs.
"""
import json
from subprocess import Popen

from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.profile import (
    ProfileManager,
    FirefoxProfile,
)
from geckordp.firefox import Firefox
from geckordp.settings import (
    GECKORDP,
    log,
)
# NOTE: enable debug logging by default
GECKORDP.DEBUG = 1
GECKORDP.DEBUG_REQUEST = 1
GECKORDP.DEBUG_RESPONSE = 1


def main(
    profile_name: str,
    host: str = 'localhost',
    port: int = 6000,

    # NOTE: optionally clone any existing profile before mutate.
    clone_existing_profile: bool = True,
    restore_from_last_session: bool = True,
    always_spawn_browser: bool = True,

) -> None:

    # clone default profile to 'geckordp'
    pm = ProfileManager()
    profile: FirefoxProfile = pm.get_profile_by_name(profile_name)

    # make a new profile if none exists by given name
    if profile is None:
        profile: FirefoxProfile = pm.create(profile_name)

    # Clone from the target profile instead of mutating it?
    # In the case where the cloned profile already exists (by
    # having a `.geckordp` suffix in the name) load that
    # (previously cloned) profile for mutation B)
    elif clone_existing_profile:

        clone_name: str = f'{profile_name}.geckordp'
        profile: FirefoxProfile = pm.get_profile_by_name(clone_name)

        # only clone if no clone already exists
        if not profile:
            profile: FirefoxProfile = pm.clone(
                profile_name,
                clone_name,
            )

    # apply low-level setts to enable RDP ctl over TCP
    # (among many other things!)
    profile.set_required_configs()

    # load the last tab set state from any prior session?
    if restore_from_last_session:
        # https://kb.mozillazine.org/Browser.startup.page#3
        profile.set_config('browser.startup.page', 3)
        profile.set_config('browser.sessionstore.resume_from_crash', True)
        profile.set_config("browser.sessionstore.restore_on_demand", True)
        profile.set_config("browser.sessionstore.restore_tabs_lazily", True)
        profile.set_config("toolkit.startup.max_resumed_crashes", 1)

    # create client and connect to firefox
    # NOTE: by default this starts a few bg worker threads!
    client = RDPClient(
        timeout_sec=0.5,
        executor_workers=1,
    )
    resp: dict | None = client.connect(host, port)
    if (
        resp is None
    ):
        if always_spawn_browser:
            # NOTE: if no firefox process can be contacted at the (host,
            # port) socket address, start firefox with specified profile
            # and RDP addr.
            proc: Popen = Firefox.start(
                "https://example.com/",
                port,
                profile.name,
                # append_args=["-headless"],
            )
            log(f'Firefox started with pid={proc.pid}')
            resp: dict | None = client.connect(
                host,
                port,
                # timeout_sec=120,
            )
            if resp is None:
                raise RuntimeError(
                    f'Could not connect to firefox instance localhost@{port}!?'
                )
        else:
            raise RuntimeError(
                f'No browser listening on RDP socket @ {(host, port)}!?'
            )

    log(f'Connected to browser @ {(host, port)} -> {resp}')

    # initialize root
    root = RootActor(client)

    # get a list of tabs
    tabs: list[dict] = root.list_tabs()
    json_tabs: str = json.dumps(tabs, indent=2)
    print(
        f'TABS ARE:\n'
        f'{json_tabs}'
    )

    # NOTE: We block here due to bg threads that were spawned in the RDPClient?
    # TODO: probably be more explicit about the concurrency here
    # since it's a bit confusing what is actually going on ;)
    # uncomment for debug/introspection if needed
    # import pdbp; pdbp.set_trace()


if __name__ == "__main__":
    # Use a project-relevant profile name if user does NOT pass
    # one as the first CLI argument.
    profile_name: str = 'geckordp'

    from sys import argv
    if len(argv) > 1:
        profile_name: str = str(argv[1])

    main(profile_name)
