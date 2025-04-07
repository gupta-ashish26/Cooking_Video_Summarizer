// static/script.js

// Progress checking for progress.html
if (window.location.pathname === '/progress') {
    window.onload = checkProgress;
    async function checkProgress() {
        const res = await fetch('/status');
        const data = await res.json();
        document.getElementById("message").innerText = data.message;
        document.getElementById("bar").style.width = data.progress + "%";

        if (data.progress < 100 && data.progress !== -1) {
            setTimeout(checkProgress, 1500);
        } else if (data.progress === 100) {
            document.getElementById("done").classList.remove('hidden');
        }
    }
}

// Drag-and-drop for index.html
if (window.location.pathname === '/') {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const form = document.getElementById('uploadForm');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => e.preventDefault());
        dropArea.addEventListener(eventName, e => e.stopPropagation());
    });

    // Highlight on dragenter/dragover
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.add('bg-blue-100');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.remove('bg-blue-100');
        });
    });

    // Handle dropped file
    dropArea.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files; // Set files in real input
        }
    });
}

async function checkProgress() {
    try {
        const res = await fetch('/status');
        const data = await res.json();

        document.getElementById("message").innerText = data.message;
        document.getElementById("bar").style.width = data.progress + "%";

        if (data.progress < 100 && data.progress !== -1) {
            setTimeout(checkProgress, 1500);
        } else if (data.progress === 100) {
            document.getElementById("done").classList.remove("hidden");
        }
    } catch (err) {
        console.error("Error fetching status:", err);
    }
}

// Trigger the function on page load
window.onload = checkProgress;
