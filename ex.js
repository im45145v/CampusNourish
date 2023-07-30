let numberOfLikes = 0;
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
  
    // Add Like button with heart icon
    const likeButton = document.createElement("button");
    likeButton.innerHTML = '<i class="fas fa-heart"></i>';
    likeButton.classList.add("like-button");
    likeButton.onclick = function() {
    likeButton.classList.toggle("liked");
    };
    postElement.appendChild(likeButton);
  
    // Add Comment section
    const commentSection = document.createElement("div");
    commentSection.classList.add("comment-section");
    commentSection.innerHTML = `
      <input type="text" placeholder="Add a comment">
      <button onclick="addComment(this)">Post</button>
      <div class="comments">
        <!-- Comments will be displayed here -->
      </div>
    `;

    
  
    document.getElementById("recentPosts").prepend(postElement);
    // Clear the input fields after posting
    document.getElementById("postText").value = "";
    document.getElementById("imageUpload").value = "";
    document.getElementById("videoUpload").value = "";
  }
  
  function addComment(commentButton) {
    const commentInput = commentButton.previousElementSibling;
    const commentText = commentInput.value;
    if (commentText) {
      const commentElement = document.createElement("div");
      commentElement.classList.add("comment");
      commentElement.innerText = commentText;
      commentButton.parentElement.querySelector(".comments").appendChild(commentElement);
      // Clear the comment input after posting
      commentInput.value = "";
    }
  }
  
