function showLoader() {
  const loader = document.getElementById("art-loader");
  if (loader) loader.style.display = "block";
}

function hideLoader() {
  const loader = document.getElementById("art-loader");
  if (loader) loader.style.display = "none";
}

function showHrForSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (!section) return;

  section.style.display = "block";

  let prev = section.previousElementSibling;
  while (prev) {
    if (prev.tagName.toLowerCase() === "hr") {
      prev.classList.add("show");
      break;
    }
    prev = prev.previousElementSibling;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  let selectedArtwork = null;
  let uploadedFilename = null;

  const artistInput = document.getElementById("artist-input");
  const suggestionsList = document.getElementById("suggestions");
  const clearBtn = document.getElementById("clear-input");
  const loadBtn = document.getElementById("load-artworks");

  loadBtn.style.display = "inline-block";
  loadBtn.disabled = true;

  artistInput.addEventListener("input", async () => {
    const q = artistInput.value.trim();

    clearBtn.style.display = artistInput.value ? "block" : "none";
    loadBtn.disabled = q.length < 3;
    loadBtn.style.display = "inline-block";

    if (q.length < 3) {
      suggestionsList.innerHTML = "";
      return;
    }

    try {
      const res = await fetch(`/api/fetch_artist?q=${encodeURIComponent(q)}`);
      const data = await res.json();

      suggestionsList.innerHTML = "";
      data.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${item.name}</strong> <em style="color:#aaa;">(${item.nationality})</em>`;
        li.style.cursor = "pointer";
        li.addEventListener("click", () => {
          artistInput.value = item.name;
          suggestionsList.innerHTML = "";
          clearBtn.style.display = "block";

          loadBtn.style.display = "inline-block";
          loadBtn.disabled = false;
        });
        suggestionsList.appendChild(li);
      });
    } catch (err) {
      console.error("Autocomplete failed", err);
    }
  });

  clearBtn.addEventListener("click", () => {
    artistInput.value = "";
    suggestionsList.innerHTML = "";
    clearBtn.style.display = "none";
    loadBtn.disabled = true;
  });

  loadBtn.addEventListener("click", async () => {
    console.log("Load Artworks clicked");
    const artist = artistInput.value.trim();
    if (!artist) {
      alert("Please select an artist.");
      return;
    }

    showLoader();

    try {
      const res = await fetch(`/api/fetch_artworks?artist=${encodeURIComponent(artist)}`);
      const data = await res.json();

      const artworksContainer = document.getElementById("artworks-container");
      const artworksList = document.getElementById("artworks-list");
      artworksList.innerHTML = "";

      if (!data.artworks || data.artworks.length === 0) {
        artworksContainer.style.display = "none";
        alert("No artworks found for this artist.");
        return;
      }

      artworksContainer.style.display = "block";
      showHrForSection("artworks-container");

      data.artworks.forEach(art => {
        const div = document.createElement("div");
        div.style.width = "180px";
        div.style.cursor = "pointer";
        div.style.border = "2px solid transparent";

        const img = document.createElement("img");
        img.src = `/style_artist/${art.filename}`;
        img.alt = art.title || "Artwork";
        img.style.width = "100%";

        const caption = document.createElement("p");
        caption.textContent = art.title || "Untitled";

        div.appendChild(img);
        div.appendChild(caption);

        div.addEventListener("click", () => {
          selectedArtwork = art.filename;
          document.getElementById("upload-section").style.display = "block";

          showHrForSection("upload-section");

          Array.from(artworksList.children).forEach(child => {
            child.style.border = "2px solid transparent";
          });
          div.style.border = "2px solid blue";
        });

        artworksList.appendChild(div);
      });
    } catch (err) {
      alert("Error loading artworks.");
      console.error(err);
    } finally {
      hideLoader();
    }
  });

  document.getElementById("apply-style").addEventListener("click", async () => {
    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];
    const applyBtn = document.getElementById("apply-style");

    if (!file) {
      alert("Please upload an image first.");
      return;
    }

    if (!selectedArtwork) {
      alert("Please select an artwork first.");
      return;
    }

    showLoader();
    applyBtn.classList.add("loading");

    try {
      const imageForm = new FormData();
      imageForm.append("file", file);

      const uploadRes = await fetch("/api/upload_image", {
        method: "POST",
        body: imageForm
      });

      if (!uploadRes.ok) throw new Error("Image upload failed.");
      const uploadData = await uploadRes.json();
      uploadedFilename = uploadData.filename;

      const styleForm = new FormData();
      styleForm.append("uploaded_filename", uploadedFilename);
      styleForm.append("style_filename", selectedArtwork);

      const styleRes = await fetch("/api/transfer_style", {
        method: "POST",
        body: styleForm
      });

      if (!styleRes.ok) throw new Error("Style transfer failed.");

      const data = await styleRes.json();
      const resultSection = document.getElementById("result-section");
      const resultImage = document.getElementById("styled-image");

      resultSection.style.display = "none";

      console.log("Respuesta del backend:", data);

      const finalImageURL = data.styled_image_url + '?t=' + new Date().getTime();
      resultImage.src = finalImageURL;


      resultImage.onload = () => {
        resultSection.style.display = "flex";

        showHrForSection("result-section");

        resultSection.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });

        const downloadBtn = document.getElementById("download-btn");
        const artistName = artistInput.value.trim().toLowerCase().replace(/\s+/g, "_");
        const filename = `artpicstyle_${artistName}.jpg`;

        downloadBtn.href = resultImage.src;
        downloadBtn.download = filename;
      };
    } catch (err) {
      alert("Failed to apply style.");
      console.error(err);
    } finally {
      hideLoader();
      applyBtn.classList.remove("loading");
    }
  });

});
