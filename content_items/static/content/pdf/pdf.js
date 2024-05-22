/* global window, tvDisplay, axios */

tvDisplay.tvContent = (function() {
  "use strict";

  let windowIntervalFn = null;

  const articleEle = tvDisplay.contentContainer.getElementsByTagName("article")[0];

  let pdfFile = "";
  let currentIndex = 0;
  let maxSlideCount = -1;

  return {
    init: function(contentJSON) {

    const nextSlide = function () {
        currentIndex += 1;

        if (currentIndex > maxSlideCount) {
          tvDisplay.next();
        } else {
          articleEle.querySelectorAll('canvas').forEach((el) => {
            el.style.display = 'none';
          })
          document.getElementById('slide_canvas' + currentIndex).style.display = 'block';
        }
      }


      const renderPage = function (pdf, pageNumber, callback) {
          let canvasEle = document.createElement("canvas");
          canvasEle.id = "slide_canvas" + pageNumber;
          articleEle.append(canvasEle);

          pdf.getPage(pageNumber).then(function (page) {
            let scale = 1;
            let viewport = page.getViewport(scale);

            let pageDisplayWidth = viewport.width;
            let pageDisplayHeight = viewport.height;

            // Prepare canvas using PDF page dimensions

            let canvas = document.getElementById("slide_canvas" + pageNumber);
            let context = canvas.getContext("2d");
            canvas.width = pageDisplayWidth;
            canvas.height = pageDisplayHeight;

            // Render PDF page into canvas context
            let renderContext = {
              canvasContext: context,
              viewport: viewport,
            };
            page.render(renderContext).promise.then(callback);

            articleEle.querySelectorAll('canvas').forEach((el) => {
                el.style.display = 'none';
            });
          });
        }

      const loadPdf = function () {
          pdfFile = tvDisplay.getContentProperty(contentJSON, "pdfFile") || "";
          const slideMillis = (tvDisplay.getContentProperty(contentJSON, "slideSeconds") || 10) * 1000;

          PDFJS.getDocument(pdfFile).then(function (pdf) {
                maxSlideCount = pdf.numPages;
                let page_number = 1;

                renderPage(pdf, page_number++, function pageRenderingComplete() {
                    if (page_number > pdf.numPages) {
                        // All pages rendered
                        if (maxSlideCount === 0) {
                              tvDisplay.next();
                          } else {
                              nextSlide();
                              windowIntervalFn = window.setInterval(nextSlide, slideMillis);
                          }
                        return;
                    }
                    // Continue rendering of the next page
                    renderPage(pdf, page_number++, pageRenderingComplete);
                });
          });
      }

      let scriptEle = document.createElement("script");
      scriptEle.src = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/1.10.100/pdf.min.js";
      scriptEle.onload = loadPdf;
      document.body.insertAdjacentElement("beforeend", scriptEle);
    },
    destroy: function() {
      try {
        window.clearInterval(windowIntervalFn);
      } catch (e) {
        // ignore
      }
    }
  };
}());
