(this.webpackJsonpsmartwindow=this.webpackJsonpsmartwindow||[]).push([[0],{1:function(t,e,n){t.exports={boxarea:"smartwindow_boxarea__2UFyo",boxoptions:"smartwindow_boxoptions__3wr-v",box:"smartwindow_box__f8U6d"}},11:function(t,e,n){},12:function(t,e,n){},15:function(t,e,n){"use strict";n.r(e);var a=n(2),l=n.n(a),i=n(5),c=n.n(i),o=(n(11),n.p,n(12),n(4)),s=n.n(o),r=n(6),d="http://192.168.0.28/";function p(){return(p=Object(r.a)(s.a.mark((function t(e){var n,a;return s.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return n=d+e,a={method:"GET"},t.next=4,fetch(n,a);case 4:case"end":return t.stop()}}),t)})))).apply(this,arguments)}var _=n(1),b=n.n(_),u=n(0),E=[{title:"Open window",call_type:"OPEN_WINDOW"},{title:"Close window",call_type:"CLOSE_WINDOW"},{title:"Trigger automated action",call_type:"PREDICT_OPERATION"},{title:"Enable close window on sunset",call_type:"ENABLE_SUNSET"},{title:"Disable close window on sunset",call_type:"DISABLE_SUNSET"},{title:"Enable open window on sunrise",call_type:"ENABLE_SUNRISE"},{title:"Disable open window on sunrise",call_type:"DISABLE_SUNRISE"},{title:"Enable gas detection",call_type:"ENABLE_GAS"},{title:"Disable gas detection",call_type:"DISABLE_GAS"}],j=[{title:"Train new predictive model",call_type:"TRAIN_PATTERN"},{title:"Reset predictive model",call_type:"RESET_PATTERN"},{title:"Enable auto smartmode",call_type:"ENABLE_SMARTMODE"},{title:"Disable auto smartmode",call_type:"DISABLE_SMARTMODE"},{title:"Enable pattern save",call_type:"ENABLE_PATTERN_SAVE"},{title:"Disable pattern save",call_type:"DISABLE_PATTERN_SAVE"}],x=function(t){var e=t.title,n=t.call_type,a=t.click,l=void 0===a?"execute":a;return Object(u.jsxs)("div",{className:b.a.box,children:[Object(u.jsx)("p",{children:e}),Object(u.jsx)("button",{onClick:function(){!function(t){p.apply(this,arguments)}(n)},children:l})]})};var w=function(){return Object(u.jsxs)(u.Fragment,{children:[Object(u.jsx)("h1",{children:"Smart Window Control Panel"}),Object(u.jsxs)("div",{className:b.a.boxarea,children:[Object(u.jsx)("b",{children:"Features"}),Object(u.jsx)("div",{className:b.a.boxoptions,children:E.map((function(t){return Object(u.jsx)(x,{title:t.title,call_type:t.call_type})}))})]}),Object(u.jsxs)("div",{className:b.a.boxarea,children:[Object(u.jsx)("b",{children:"Advanced Settings"}),Object(u.jsx)("div",{className:b.a.boxoptions,children:j.map((function(t){return Object(u.jsx)(x,{title:t.title,call_type:t.call_type})}))})]})]})};var O=function(){return Object(u.jsx)("div",{className:"App",children:Object(u.jsx)(w,{})})},m=function(t){t&&t instanceof Function&&n.e(3).then(n.bind(null,16)).then((function(e){var n=e.getCLS,a=e.getFID,l=e.getFCP,i=e.getLCP,c=e.getTTFB;n(t),a(t),l(t),i(t),c(t)}))};c.a.render(Object(u.jsx)(l.a.StrictMode,{children:Object(u.jsx)(O,{})}),document.getElementById("root")),m()}},[[15,1,2]]]);
//# sourceMappingURL=main.d37ec779.chunk.js.map