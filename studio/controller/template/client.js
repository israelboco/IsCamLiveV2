const videoElement = document.getElementById('videoElement');
const audioElement = document.getElementById('audioElement');

async function startVideo() {
    try {
        // Récupérer le flux vidéo depuis le serveur
        const videoStream = await fetch('http://<IP_DU_PC_DISTANT>:5000/video_feed').then(response => response.blob());
        videoElement.src = URL.createObjectURL(videoStream);

        // Récupérer le flux audio depuis le serveur
        const audioStream = await fetch('http://<IP_DU_PC_DISTANT>:5000/audio_feed').then(response => response.blob());
        audioElement.src = URL.createObjectURL(audioStream);
    } catch (error) {
        console.error('Erreur lors de la récupération des flux :', error);
    }
}

startVideo();
