"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.patchStrictSandbox = patchStrictSandbox;
var _utils = require("../../../utils");
var _common = require("../../common");
var _common2 = require("./common");
/**
 * @author Kuitos
 * @since 2020-10-13
 */

// Get native global window with a sandbox disgusted way, thus we could share it between qiankun instances🤪
Object.defineProperty(_utils.nativeGlobal, '__proxyAttachContainerConfigMap__', {
  enumerable: false,
  writable: true
});
// Share proxyAttachContainerConfigMap between multiple qiankun instance, thus they could access the same record
_utils.nativeGlobal.__proxyAttachContainerConfigMap__ = _utils.nativeGlobal.__proxyAttachContainerConfigMap__ || new WeakMap();
var proxyAttachContainerConfigMap = _utils.nativeGlobal.__proxyAttachContainerConfigMap__;
var elementAttachContainerConfigMap = new WeakMap();
var docCreatePatchedMap = new WeakMap();
function patchDocumentCreateElement() {
  var docCreateElementFnBeforeOverwrite = docCreatePatchedMap.get(document.createElement);
  if (!docCreateElementFnBeforeOverwrite) {
    var rawDocumentCreateElement = document.createElement;
    Document.prototype.createElement = function createElement(tagName, options) {
      var element = rawDocumentCreateElement.call(this, tagName, options);
      if ((0, _common2.isHijackingTag)(tagName)) {
        var _ref = (0, _common.getCurrentRunningApp)() || {},
          currentRunningSandboxProxy = _ref.window;
        if (currentRunningSandboxProxy) {
          var proxyContainerConfig = proxyAttachContainerConfigMap.get(currentRunningSandboxProxy);
          if (proxyContainerConfig) {
            elementAttachContainerConfigMap.set(element, proxyContainerConfig);
          }
        }
      }
      return element;
    };
    // It means it have been overwritten while createElement is an own property of document
    if (document.hasOwnProperty('createElement')) {
      document.createElement = Document.prototype.createElement;
    }
    docCreatePatchedMap.set(Document.prototype.createElement, rawDocumentCreateElement);
  }
  return function unpatch() {
    if (docCreateElementFnBeforeOverwrite) {
      Document.prototype.createElement = docCreateElementFnBeforeOverwrite;
      document.createElement = docCreateElementFnBeforeOverwrite;
    }
  };
}
function patchStrictSandbox(appName, appWrapperGetter, proxy) {
  var mounting = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : true;
  var scopedCSS = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : false;
  var excludeAssetFilter = arguments.length > 5 ? arguments[5] : undefined;
  var speedySandbox = arguments.length > 6 && arguments[6] !== undefined ? arguments[6] : false;
  var containerConfig = proxyAttachContainerConfigMap.get(proxy);
  if (!containerConfig) {
    containerConfig = {
      appName: appName,
      proxy: proxy,
      appWrapperGetter: appWrapperGetter,
      dynamicStyleSheetElements: [],
      strictGlobal: true,
      speedySandbox: speedySandbox,
      excludeAssetFilter: excludeAssetFilter,
      scopedCSS: scopedCSS
    };
    proxyAttachContainerConfigMap.set(proxy, containerConfig);
  }
  // all dynamic style sheets are stored in proxy container
  var _containerConfig = containerConfig,
    dynamicStyleSheetElements = _containerConfig.dynamicStyleSheetElements;
  var unpatchDocumentCreate = patchDocumentCreateElement();
  var unpatchDynamicAppendPrototypeFunctions = (0, _common2.patchHTMLDynamicAppendPrototypeFunctions)(function (element) {
    return elementAttachContainerConfigMap.has(element);
  }, function (element) {
    return elementAttachContainerConfigMap.get(element);
  });
  if (!mounting) (0, _common2.calcAppCount)(appName, 'increase', 'bootstrapping');
  if (mounting) (0, _common2.calcAppCount)(appName, 'increase', 'mounting');
  return function free() {
    if (!mounting) (0, _common2.calcAppCount)(appName, 'decrease', 'bootstrapping');
    if (mounting) (0, _common2.calcAppCount)(appName, 'decrease', 'mounting');
    // release the overwritten prototype after all the micro apps unmounted
    if ((0, _common2.isAllAppsUnmounted)()) {
      unpatchDynamicAppendPrototypeFunctions();
      unpatchDocumentCreate();
    }
    (0, _common2.recordStyledComponentsCSSRules)(dynamicStyleSheetElements);
    // As now the sub app content all wrapped with a special id container,
    // the dynamic style sheet would be removed automatically while unmoutting
    return function rebuild() {
      (0, _common2.rebuildCSSRules)(dynamicStyleSheetElements, function (stylesheetElement) {
        var appWrapper = appWrapperGetter();
        if (!appWrapper.contains(stylesheetElement)) {
          var mountDom = stylesheetElement[_common2.styleElementTargetSymbol] === 'head' ? (0, _common2.getAppWrapperHeadElement)(appWrapper) : appWrapper;
          _common2.rawHeadAppendChild.call(mountDom, stylesheetElement);
          return true;
        }
        return false;
      });
    };
  };
}