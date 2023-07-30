function addPost() {
    const postText = document.getElementById("postText").value;
  
    const postElement = document.createElement("div");
    postElement.classList.add("post");
  
    if (postText) {
      const textElement = document.createElement("p");
      textElement.innerText = postText;
      postElement.appendChild(textElement);
    }
  
    const imageFile = document.getElementById("imageUpload").files[0];
    if (imageFile) {
      const imageElement = document.createElement("img");
      imageElement.src = URL.createObjectURL(imageFile);
      postElement.appendChild(imageElement);
    }
  
    const videoFile = document.getElementById("videoUpload").files[0];
    if (videoFile) {
      const videoElement = document.createElement("video");
      videoElement.src = URL.createObjectURL(videoFile);
      videoElement.width = "560";
      videoElement.height = "315";
      videoElement.controls = true;
      postElement.appendChild(videoElement);
    }
  
    document.getElementById("recentPosts").prepend(postElement);
    // Clear the input fields after posting
    document.getElementById("postText").value = "";
    document.getElementById("imageUpload").value = "";
    document.getElementById("videoUpload").value = "";
  }
  