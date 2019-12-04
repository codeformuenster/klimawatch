// Header
const header = document.querySelector("header");

window.addEventListener("load", () => {
  document.body.style.paddingTop = `${header.offsetHeight}px`;

  const anchors = document.querySelectorAll("a");
  for (const anchor of anchors) {
    if (anchor.href.startsWith("mailto:")) {
      const [address, ...rest] = anchor.href.slice(7).split("?");
      const reversed = address
        .split("")
        .reverse()
        .join("");
      anchor.href = `mailto:${reversed}${
        rest.length !== 0 ? `?${rest.join("")}` : ""
      }`;
      if (anchor.textContent.trim() === address) {
        anchor.textContent = reversed;
      }
    }
  }
});
