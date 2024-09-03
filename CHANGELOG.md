###### Labels:

<sub>[breaking] - backward incompatible API changes<sub>

<br>

## 1.0.3
- introduce semantic versioning
- [breaking] Events.RESOURCE_AVAILABLE_FROM changed to Events.RESOURCES_AVAILABLE_ARRAY 
  with new data structure
- run tests on Firefox 129.0 successfully

## 0.5.0
- add universal listener
- add ThreadConfigurationActor
- fix storage related issues
- run tests on Firefox 126.0 successfully

## 0.4.53
- remove EventSourceActor
- remove StorageActor
- update RootActor
- update WindowGlobalActor
- run tests on Firefox 113.0 successfully

## 0.4.44
- update WebConsoleActor
- ProfileManager improvements
- run tests on Firefox 110.0 successfully

## 0.4.42
- internal refactoring for explicit typing
- update to Python 3.10
- fix possible errors in RDPClient

## 0.4.38
- fix release signatures

## 0.4.35
- introduce releases and signatures

## 0.4.30
- add StorageActor
- add CacheStorageActor
- add CookieStorageActor
- add ExtensionStorageActor
- add IndexedDBStorageActor
- add LocalStorageActor
- add SessionStorageActor
- update WatcherActor

## 0.4.26
- deprecated PerformanceActor removed
- ProfileManager improvements
- run tests on Firefox 106.0 successfully

## 0.4.4
- update WindowGlobalActor
- update WalkerActor
- update NodeActor

## 0.4.3
- rename BrowsingContext to WindowGlobal
- update WalkerActor

## 0.4.1
- repackage

## 0.4.0
- add HeapSnapshotActor
- add MemoryActor
- add support for bulk responses

## 0.3.0
- add NodeActor
- add NodeListActor
- add AccessibilityActor
- add AccessibleWalkerActor
- add AccessibleActor
- add ParentAccessibilityActor
- add SimulatorActor
- add PerformanceActor
- add missing tests for WalkerActor
- refactor README Development section and dev/ directory
- add profile manager CLI tool to dev/profile.py

## 0.1.13
- cleanup package
- refactor profile and fix permission and access errors on specific edge cases
- run tests on Firefox 90.0 successfully

## 0.1.12
- refactor webconsole preferences functions, docs and tests
- added events registration for jmespath expressions
- test profiles are removed afterwards

## 0.1.11
- fix Firefox.start()
- firefox paths for macos corrected

## 0.1.10
- refactored documents

## 0.1.9
- fix missing modules

## 0.1.8
- fix pypi package
- refactored documents

## 0.1.7
- initial release