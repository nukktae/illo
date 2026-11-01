// Minimal renderer for the canvas screen format, so the screens run as plain static HTML.
// Supports {{ path }} holes in text and attributes, <sc-if value>, <sc-for list as>,
// on* event holes, and a DCLogic base class with setState.
(function () {
  function lookup(expr, scope) {
    expr = expr.trim();
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
    return expr.split('.').reduce(function (o, k) { return o == null ? undefined : o[k]; }, scope);
  }

  var HOLE = /\{\{([^}]+)\}\}/g;
  var ONLY_HOLE = /^\s*\{\{([^}]+)\}\}\s*$/;

  function interp(text, scope) {
    return text.replace(HOLE, function (_, e) {
      var v = lookup(e, scope);
      return v == null ? '' : String(v);
    });
  }

  function build(node, scope, out) {
    if (node.nodeType === 3) {
      out.appendChild(document.createTextNode(interp(node.nodeValue, scope)));
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.tagName.toLowerCase();
    if (tag === 'sc-if') {
      if (lookup(node.getAttribute('value').replace(/[{}]/g, ''), scope)) {
        node.childNodes.forEach(function (c) { build(c, scope, out); });
      }
      return;
    }
    if (tag === 'sc-for') {
      var list = lookup(node.getAttribute('list').replace(/[{}]/g, ''), scope) || [];
      var as = node.getAttribute('as');
      list.forEach(function (item) {
        var inner = Object.create(scope);
        inner[as] = item;
        node.childNodes.forEach(function (c) { build(c, inner, out); });
      });
      return;
    }
    var el = node.namespaceURI === 'http://www.w3.org/1999/xhtml'
      ? document.createElement(node.localName)
      : document.createElementNS(node.namespaceURI, node.localName);
    Array.prototype.forEach.call(node.attributes, function (a) {
      var name = a.name, val = a.value, m = val.match(ONLY_HOLE);
      if (/^on/i.test(name) && m) {
        var fn = lookup(m[1], scope);
        if (typeof fn === 'function') el.addEventListener(name.slice(2).toLowerCase(), fn);
        return;
      }
      if (name.indexOf('hint-') === 0) return;
      el.setAttribute(name, interp(val, scope));
    });
    var src = tag === 'template' ? node.content : node;
    src.childNodes.forEach(function (c) { build(c, scope, el); });
    if (tag === 'textarea') el.value = el.textContent;
    out.appendChild(el);
  }

  window.DCLogic = function DCLogic(props) { this.props = props || {}; this.state = {}; };
  window.DCLogic.prototype.renderVals = function () { return {}; };
  window.DCLogic.prototype.setState = function (patch) {
    Object.assign(this.state, typeof patch === 'function' ? patch(this.state) : patch);
    this._render();
  };

  window.DC = {
    mount: function (Component) {
      var tpl = document.getElementById('dc').content;
      var app = document.getElementById('app');
      var comp = new Component({});
      comp._render = function () {
        var frag = document.createDocumentFragment();
        var scope = comp.renderVals();
        tpl.childNodes.forEach(function (c) { build(c, scope, frag); });
        app.replaceChildren(frag);
      };
      comp._render();
    }
  };
})();
