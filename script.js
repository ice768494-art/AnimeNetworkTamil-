const updatesGrid = document.getElementById("updatesGrid");
const searchInput = document.getElementById("searchInput");
const refreshBtn = document.getElementById("refreshBtn");
const statusText = document.getElementById("statusText");

let posts = [];

async function loadPosts() {
    try {
        statusText.textContent = "Loading...";

        const response = await fetch("/api/posts");

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        posts = data.posts || [];

        renderPosts(posts);

        statusText.textContent =
            `${posts.length} update${posts.length === 1 ? "" : "s"}`;

    } catch (error) {
        console.error(error);

        statusText.textContent = "Unable to load updates";

        updatesGrid.innerHTML = `
            <div class="empty">
                <h3>Database connection unavailable</h3>
                <p>Check your Supabase environment variables.</p>
            </div>
        `;
    }
}

function renderPosts(items) {
    if (!items.length) {
        updatesGrid.innerHTML = `
            <div class="empty">
                <h3>No anime updates yet</h3>
                <p>New Telegram posts will appear here.</p>
            </div>
        `;
        return;
    }

    updatesGrid.innerHTML = items.map(post => `
        <article class="anime-card">

            ${
                post.image_url
                ? `<img src="${escapeHtml(post.image_url)}"
                        alt="${escapeHtml(post.title || "Anime")}"
                        loading="lazy">`
                : `<div class="poster-placeholder">🎬</div>`
            }

            <div class="card-content">

                <h3>
                    ${escapeHtml(post.title || "Anime Update")}
                </h3>

                <p>
                    ${escapeHtml(
                        post.content || "New anime update available."
                    )}
                </p>

                <div class="card-footer">

                    ${
                        post.message_url
                        ? `<a href="${escapeHtml(post.message_url)}"
                              target="_blank"
                              rel="noopener">
                              View on Telegram
                           </a>`
                        : ""
                    }

                    ${
                        post.published_at
                        ? `<small>
                            ${formatDate(post.published_at)}
                           </small>`
                        : ""
                    }

                </div>

            </div>

        </article>
    `).join("");
}

function filterPosts() {
    const query = searchInput.value.toLowerCase().trim();

    const filtered = posts.filter(post => {
        const title = post.title || "";
        const content = post.content || "";
        const category = post.category || "";

        return (
            title.toLowerCase().includes(query) ||
            content.toLowerCase().includes(query) ||
            category.toLowerCase().includes(query)
        );
    });

    renderPosts(filtered);
}

function formatDate(value) {
    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "";
    }

    return date.toLocaleDateString();
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

searchInput?.addEventListener("input", filterPosts);

refreshBtn?.addEventListener("click", loadPosts);

loadPosts();
