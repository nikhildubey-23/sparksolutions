document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    // Unique fade-in and glow animation for hero tagline on home page
    const taglineElement = document.getElementById('hero-tagline');
    if (taglineElement && path === '/') {
        taglineElement.style.opacity = '0';
        taglineElement.style.animation = 'fadeInGlow 2s ease-in-out forwards';
    }

    // Scroll reveal animations
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-rotate');
    function revealOnScroll() {
        const windowHeight = window.innerHeight;
        revealElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const revealPoint = 150;
            if (elementTop < windowHeight - revealPoint) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        });
    }
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll();

    // Footer animation on scroll
    const footer = document.querySelector('.footer');
    if (footer) {
        const footerObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    footer.classList.add('footer-visible');
                }
            });
        }, { threshold: 0.1 });
        footerObserver.observe(footer);
    }

    // 3D background animation setup with different geometries per page
    if (window.THREE) {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0); // transparent background
        document.body.appendChild(renderer.domElement);
        renderer.domElement.style.position = 'fixed';
        renderer.domElement.style.top = 0;
        renderer.domElement.style.left = 0;
        renderer.domElement.style.zIndex = '-1';

        let geometry, material, mesh, rotationSpeedX = 0.01, rotationSpeedY = 0.01, color = 0x007bff;

        if (path === '/') {
            // Home: Torus
            geometry = new THREE.TorusGeometry(10, 3, 16, 100);
        } else if (path === '/services') {
            // Services: Box
            geometry = new THREE.BoxGeometry(10, 10, 10);
            rotationSpeedX = 0.005;
            rotationSpeedY = 0.015;
            color = 0x28a745;
        } else if (path === '/portfolio') {
            // Portfolio: Sphere
            geometry = new THREE.SphereGeometry(8, 32, 32);
            rotationSpeedX = 0.02;
            rotationSpeedY = 0.01;
            color = 0x6f42c1;
        } else if (path === '/contact') {
            // Contact: Cylinder
            geometry = new THREE.CylinderGeometry(5, 5, 15, 32);
            rotationSpeedX = 0.01;
            rotationSpeedY = 0.02;
            color = 0xfd7e14;
        } else if (path === '/docs') {
            // Docs: TorusKnot
            geometry = new THREE.TorusKnotGeometry( 10, 3, 100, 16 );
            rotationSpeedX = 0.015;
            rotationSpeedY = 0.005;
            color = 0x00FFFF;
        } else {
            // Default: Torus
            geometry = new THREE.TorusGeometry(10, 3, 16, 100);
        }

        material = new THREE.MeshBasicMaterial({ color: color, wireframe: true });
        mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        camera.position.z = 30;

        function animate() {
            requestAnimationFrame(animate);
            mesh.rotation.x += rotationSpeedX;
            mesh.rotation.y += rotationSpeedY;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth/window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }
});
