from enum import Enum


class Events():
    """ A list of all events which can be received by the rdp server.

        These events will be once registered in 'RDPClient' to handle responses.
    """

    class Accessible(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L46
        """
        ACTIONS_CHANGE = "actionsChange"
        NAME_CHANGE = "nameChange"
        VALUE_CHANGE = "valueChange"
        DESCRIPTION_CHANGE = "descriptionChange"
        STATES_CHANGE = "statesChange"
        ATTRIBUTES_CHANGE = "attributesChange"
        SHORTCUT_CHANGE = "shortcutChange"
        REORDER = "reorder"
        TEXT_CHANGE = "textChange"
        INDEX_IN_PARENT_CHANGE = "indexInParentChange"
        AUDITED = "audited"

    class AccessibleWalker(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L130
        """
        DOCUMENT_READY = "documentReady"
        PICKER_ACCESSIBLE_PICKED = "pickerAccessiblePicked"
        PICKER_ACCESSIBLE_PREVIEWED = "pickerAccessiblePreviewed"
        PICKER_ACCESSIBLE_HOVERED = "pickerAccessibleHovered"
        PICKER_ACCESSIBLE_CANCELED = "pickerAccessibleCanceled"
        HIGHLIGHTER_EVENT = "highlighter-event"
        AUDIT_EVENT = "audit-event"

    class Accessibility(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L225
        """
        INIT = "init"
        SHUTDOWN = "shutdown"

    class Browser(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/targets/browsing-context.js
        """
        TAB_NAVIGATED = "tabNavigated"
        FRAME_UPDATE = "frameUpdate"
        TAB_DETACHED = "tabDetached"
        WORKER_LIST_CHANGED = "workerListChanged"

    class ContentProcess(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/targets/content-process.js
        """
        WORKER_LIST_CHANGED = "workerListChanged"
        TAB_DETACHED = "tabDetached"

    class EventSource(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/eventsource.js
        """
        EVENT_SOURCE_CONNECTION_CLOSED = "eventSourceConnectionClosed"
        EVENT_RECEIVED = "eventReceived"

    class Inspector(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/inspector.js
        """
        COLOR_PICKED = "colorPicked"
        COLOR_PICK_CANCELED = "colorPickCanceled"

    class Memory(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/memory.js
        """
        GARBAGE_COLLECTION = "garbage-collection"
        ALLOCATIONS = "allocations"

    class Network(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/network-event.js
        """
        NETWORK_EVENT_UPDATE = "networkEventUpdate"

    class ParentAccessibility(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L263
        """
        INIT = "canBeDisabledChange"
        SHUTDOWN = "canBeEnabledChange"

    class Performance(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/performance.js
        """
        RECORDING_STARTED = "recording-started"
        RECORDING_STOPPING = "recording-stopping"
        RECORDING_STOPPED = "recording-stopped"
        PROFILER_STATUS = "profiler-status"
        CONSOLE_PROFILE_START = "console-profile-start"
        TIMELINE_DATA = "timeline-data"

    class Process(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/process.js
        """
        DESCRIPTOR_DESTROYED = "descriptor-destroyed"

    class Root(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/root.js
        """
        TAB_LIST_CHANGED = "tabListChanged"
        WORKER_LIST_CHANGED = "workerListChanged"
        ADDON_LIST_CHANGED = "addonListChanged"
        SERVICE_WORKER_REGISTRATION_LIST_CHANGED = "serviceWorkerRegistrationListChanged"
        PROCESS_LIST_CHANGED = "processListChanged"

    class Storage(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
        """
        STORES_UPDATE = "storesUpdate"
        STORES_CLEARED = "storesCleared"
        STORES_RELOADED = "storesReloaded"

    class Thread(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/thread.js
        """
        PAUSED = "paused"
        RESUMED = "resumed"
        WILL_INTERRUPT = "willInterrupt"
        NEW_SOURCE = "newSource"

    class Walker(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/walker.js
        """
        NEW_MUTATIONS = "newMutations"
        ROOT_AVAILABLE = "root-available"
        ROOT_DESTROYED = "root-destroyed"
        PICKER_NODE_PICKED = "pickerNodePicked"
        PICKER_NODE_PREVIEWED = "pickerNodePreviewed"
        PICKER_NODE_HOVERED = "pickerNodeHovered"
        PICKER_NODE_CANCELED = "pickerNodeCanceled"
        DISPLAY_CHANGE = "display-change"
        SCROLLABLE_CHANGE = "scrollable-change"
        OVERFLOW_CHANGE = "overflow-change"
        RESIZE = "resize"

    class Watcher(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/watcher.js
            events reside in webconsole, however its origin (and its actor) comes actually from watcher
        """
        TARGET_AVAILABLE_FORM = "target-available-form"
        TARGET_DESTROYED_FORM = "target-destroyed-form"
        RESOURCE_AVAILABLE_FORM = "resource-available-form"
        RESOURCE_DESTROYED_FORM = "resource-destroyed-form"
        RESOURCE_UPDATED_FORM = "resource-updated-form"

    class WebConsole(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/webconsole.js
        """
        EVALUATION_RESULT = "evaluationResult"
        FILE_ACTIVITY = "fileActivity"
        PAGE_ERROR = "pageError"
        LOG_MESSAGE = "logMessage"
        CONSOLE_API_CALL = "consoleAPICall"
        REFLOW_ACTIVITY = "reflowActivity"
        NETWORK_EVENT = "networkEvent"
        INSPECT_OBJECT = "inspectObject"
        LAST_PRIVATE_CONTEXT_EXITED = "lastPrivateContextExited"
        DOCUMENT_EVENT = "documentEvent"

    class WebSocket(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/websocket.js
        """
        WEB_SOCKET_OPENED = "webSocketOpened"
        WEB_SOCKET_CLOSED = "webSocketClosed"
        FRAME_RECEIVED = "frameReceived"
        FRAME_SENT = "frameSent"

    class Worker(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/worker.js
        """
        DESCRIPTOR_DESTROYED = "descriptor-destroyed"
