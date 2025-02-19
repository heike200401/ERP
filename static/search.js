document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchSuggestions = document.getElementById('search-suggestions');

    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        if (query.length > 0) {
            fetch(`/search/suggest?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    searchSuggestions.innerHTML = data.map(item => `
                        <a href="${item.url}">
                            <span class="result-type">${item.type}</span>
                            <span class="result-name">${item.name}</span>
                        </a>
                    `).join('');
                    searchSuggestions.style.display = 'block';
                });
        } else {
            searchSuggestions.innerHTML = '';
            searchSuggestions.style.display = 'none';
        }
    });

    // 点击页面其他区域时隐藏搜索建议
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchSuggestions.contains(event.target)) {
            searchSuggestions.style.display = 'none';
        }
    });
}); 