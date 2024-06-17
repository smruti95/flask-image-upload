document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const uploadForm = document.getElementById('upload-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            if (response.status === 200) {
                localStorage.setItem('token', data.access_token);
                window.location.href = '/upload';
            } else {
                document.getElementById('error-message').innerText = data.msg;
            }
        });
    }

    if (uploadForm) {
        console.log();
        uploadForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const fileInput = document.querySelector('input[type="file"]');
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            const token = localStorage.getItem('token');
            console.log(token);
            const response = await fetch('/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            const data = await response.json();
            if (response.status === 200) {
                window.location.href = `/uploaded/${data.filename}`;
            } else {
                document.getElementById('upload-message').innerText = 'Upload failed';
            }
        });
    }
});
