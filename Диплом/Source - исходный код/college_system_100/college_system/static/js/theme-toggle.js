document.addEventListener("DOMContentLoaded", () => {
  // Тема (светлая/темная)
  const btn = document.getElementById("themeToggle");
  const root = document.documentElement;

  if (root) {
    const saved = localStorage.getItem("theme") || "light";
    root.setAttribute("data-bs-theme", saved);
  }

  if (btn && root) {
    btn.addEventListener("click", () => {
      const current =
        root.getAttribute("data-bs-theme") === "dark" ? "dark" : "light";
      const next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-bs-theme", next);
      localStorage.setItem("theme", next);
    });
  }

  // Плавное появление блоков при скролле
  const animated = document.querySelectorAll(".fade-in-up");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const delay = el.getAttribute("data-delay") || 0;
            setTimeout(() => {
              el.classList.add("is-visible");
            }, Number(delay));
            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.1 }
    );

    animated.forEach((el) => observer.observe(el));
  } else {
    // Fallback: показать все сразу
    animated.forEach((el) => el.classList.add("is-visible"));
  }
});


