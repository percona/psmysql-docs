document.addEventListener("DOMContentLoaded", function () {
    // Check if widget was closed before
    const closedUntil = localStorage.getItem("feedbackWidgetClosedUntil");
    if (closedUntil && new Date().getTime() < parseInt(closedUntil, 10)) {
      return; // Don't show widget if closed and timer not expired
    }
  
    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.bottom = "20px";
    container.style.right = "20px";
    container.style.background = "#fff";
    container.style.border = "1px solid #ddd";
    container.style.padding = "10px 15px";
    container.style.borderRadius = "8px";
    container.style.boxShadow = "0 2px 6px rgba(0,0,0,0.15)";
    container.style.zIndex = 9999;
    container.style.fontFamily = '"Poppins", "Roboto", Arial, Helvetica, sans-serif';
    container.style.textAlign = "center";
    container.style.width = "250px";
  
    // Close button
    const closeBtn = document.createElement("button");
    closeBtn.innerText = "×";
    closeBtn.style.position = "absolute";
    closeBtn.style.top = "-2px";      // push close button slightly above the container edge
    closeBtn.style.right = "-2px";    // push close button slightly outside right edge
    closeBtn.style.border = "none";
    closeBtn.style.background = "transparent";
    closeBtn.style.fontSize = "24px"; 
    closeBtn.style.cursor = "pointer";
    closeBtn.style.color = "#999";
    closeBtn.style.fontWeight = "bold";
    closeBtn.style.lineHeight = "1";
    closeBtn.style.padding = "0";
    closeBtn.style.width = "30px";
    closeBtn.style.height = "30px";
  
    closeBtn.addEventListener("click", () => {
      container.style.display = "none";
      // Hide for 4 hours
      const fourHoursFromNow = new Date().getTime() + 4 * 60 * 60 * 1000;
      localStorage.setItem("feedbackWidgetClosedUntil", fourHoursFromNow.toString());
    });
  
    container.appendChild(closeBtn);
  
    const title = document.createElement("div");
    title.innerText = "Do you like Percona docs?";
    title.style.marginBottom = "8px";
    title.style.fontSize = "14px";
    title.style.fontWeight = "bold";
    title.style.color = "#0E5FB5";
    title.style.fontFamily = '"Poppins", "Roboto", Arial, Helvetica, sans-serif';
    container.appendChild(title);
  
    const stars = document.createElement("div");
    stars.style.position = "relative";
  
    for (let i = 1; i <= 5; i++) {
      const star = document.createElement("span");
      star.innerHTML = "☆";
      star.style.fontSize = "24px";
      star.style.cursor = "pointer";
      star.style.margin = "0 3px";
      star.style.color = "#000";
  
      star.addEventListener("mouseover", () => {
        [...stars.children].forEach((s, index) => {
          s.innerHTML = index < i ? "★" : "☆";
          s.style.color = index < i ? "#0E5FB5" : "#000";
        });
      });
  
      star.addEventListener("mouseleave", () => {
        [...stars.children].forEach((s) => {
          s.innerHTML = "☆";
          s.style.color = "#000";
        });
      });
  
      star.addEventListener("click", () => {
        const formURL = "https://docs.google.com/forms/d/e/1FAIpQLSfhscELpzoXB4uyh9pXNmXSeqKc10IH_DxmAoaVGID85sO0Aw/viewform";
        const ratingURL = `${formURL}?entry.303027158=${i}`;
        window.open(ratingURL, "_blank");
      });
  
      stars.appendChild(star);
    }
  
    container.appendChild(stars);
    document.body.appendChild(container);
  });
  