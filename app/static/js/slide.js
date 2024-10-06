document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    slides.forEach((slide, index) => {
        const prevBtn = slide.querySelector('.prevBtn');
        const nextBtn = slide.querySelector('.nextBtn');

        prevBtn.addEventListener('click', function() {
            showSlide(index - 1);
        });

        nextBtn.addEventListener('click', function() {
            showSlide(index + 1);
        });
    });

    function showSlide(index) {
        currentSlide = (index + slides.length) % slides.length;
        slides.forEach((slide, i) => {
            if (i === currentSlide) {
                slide.style.display = 'block';
            } else {
                slide.style.display = 'none';
            }
        });
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    function prevSlide() {
        showSlide(currentSlide - 1);
    }

    setInterval(nextSlide, 3000); // Cambia 2000 por el intervalo de tiempo en milisegundos entre cada slide
    showSlide(0);
  });