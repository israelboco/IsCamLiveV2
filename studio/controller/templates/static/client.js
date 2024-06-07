const videoElement = document.getElementById('videoElement');
const audioElement = document.getElementById('audioElement');
const client_ip = document.getElementById('client_ip');

async function startVideo() {
    try {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('Access-Control-Allow-Origin', '*');
        headers.append('Access-Control-Allow-Credentials', 'true');
        headers.append('GET', 'POST', 'OPTIONS');
        // Récupérer le flux vidéo depuis le serveur
        const videoStream = await fetch('http://'+ client_ip.innerHTML +':5000/camlive/video_feed',
            {
                mode: 'cors',
                credentials: 'include',
                // method: 'POST',
                headers: headers
            }
        ).then(response => response.blob());
        console.log(client_ip.innerHTML)
        videoElement.src = URL.createObjectURL(videoStream);

        // Récupérer le flux audio depuis le serveur
        const audioStream = await fetch('http://'+ client_ip.innerHTML +':5000/camlive/audio_feed',
            {
                mode: 'cors',
                credentials: 'include',
                // method: 'POST',
                headers: headers
            }
        ).then(response => response.blob());
        audioElement.src = URL.createObjectURL(audioStream);
    } catch (error) {
        console.error('Erreur lors de la récupération des flux :', error);
    }
}

startVideo();
