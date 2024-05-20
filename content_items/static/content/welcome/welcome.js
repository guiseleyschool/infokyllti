/* global window, tvDisplay, axios */

tvDisplay.tvContent = (function () {
  "use strict";

  const welcomeEle =
    tvDisplay.contentContainer.getElementsByTagName("article")[0];
  const displayIDEle = welcomeEle.getElementsByClassName("displayID")[0];

  return {
    init: function (contentJSON) {
      displayIDEle.innerHTML = tvDisplay.displayID;
      for (let i = 1; i <= 100; i++) {
        welcomeEle.innerHTML +=
          "<div class='circle-container'><div class='circle'></div></div>";
      }
    },
  };
})();
