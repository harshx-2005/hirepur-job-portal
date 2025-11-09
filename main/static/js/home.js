document.addEventListener('DOMContentLoaded', function() {
    // Apply Filters Button
    const applyFiltersBtn = document.querySelector('.apply-filters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            const baseUrl = window.location.pathname;
            const queryParams = new URLSearchParams();
            
            // Get all checked filters
            document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
                if (queryParams.has(checkbox.name)) {
                    queryParams.append(checkbox.name, checkbox.value);
                } else {
                    queryParams.set(checkbox.name, checkbox.value);
                }
            });
            
            // Preserve search query if exists
            const searchQuery = new URLSearchParams(window.location.search).get('q');
            if (searchQuery) {
                queryParams.set('q', searchQuery);
            }
            
            window.location.href = `${baseUrl}?${queryParams.toString()}`;
        });
    }

    // Clear Filters Button - Fix
const clearFiltersBtn = document.querySelector('.clear-filters');
if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener('click', function() {
        const baseUrl = window.location.pathname;
        const queryParams = new URLSearchParams(window.location.search);
        
        // Remove all filter parameters but keep search query if exists
        const searchQuery = queryParams.get('q');
        const sort = queryParams.get('sort');
        
        let newUrl = baseUrl;
        const newParams = new URLSearchParams();
        
        if (searchQuery) newParams.set('q', searchQuery);
        if (sort) newParams.set('sort', sort);
        
        if (newParams.toString()) {
            newUrl += `?${newParams.toString()}`;
        }
        
        window.location.href = newUrl;
    });
}
    
    // Reset Search Button
    const resetSearchBtn = document.querySelector('.reset-search');
    if (resetSearchBtn) {
        resetSearchBtn.addEventListener('click', function() {
            window.location.href = window.location.pathname;
        });
    }
    
    // Apply for Job Modal
    const applyModal = document.getElementById('apply-modal');
    const applyBtns = document.querySelectorAll('.apply-btn');
    const closeModal = document.querySelector('.close-modal');
    
    if (applyBtns.length && applyModal) {
        applyBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const jobId = this.getAttribute('data-job-id');
                const jobTitle = this.getAttribute('data-job-title');
                
                document.getElementById('job-title-modal').textContent = jobTitle;
                document.getElementById('job-id-input').value = jobId;
                
                applyModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });
        
        closeModal.addEventListener('click', function() {
            applyModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
        
        window.addEventListener('click', function(e) {
            if (e.target === applyModal) {
                applyModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }
    
    // Handle form submission
    const applicationForm = document.getElementById('application-form');
    if (applicationForm) {
        applicationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const jobId = formData.get('job_id');
            
            fetch('/apply-job/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI to show applied status
                    const applyBtn = document.querySelector(`.apply-btn[data-job-id="${jobId}"]`);
                    if (applyBtn) {
                        applyBtn.innerHTML = '<i class="fas fa-check"></i> Applied';
                        applyBtn.classList.add('applied');
                        applyBtn.disabled = true;
                    }
                    
                    // Close modal
                    applyModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    
                    // Show success message
                    alert('Application submitted successfully!');
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting your application.');
            });
        });
    }
    
    /* Sort dropdown functionality
    const sortDropdown = document.getElementById('sort-jobs');
    if (sortDropdown) {
        sortDropdown.addEventListener('change', function() {
            const baseUrl = window.location.pathname;
            const queryParams = new URLSearchParams(window.location.search);
            queryParams.set('sort', this.value);
            window.location.href = `${baseUrl}?${queryParams.toString()}`;
        });
        
        // Set current sort value from URL
        const urlParams = new URLSearchParams(window.location.search);
        const currentSort = urlParams.get('sort');
        if (currentSort) {
            sortDropdown.value = currentSort;
        }
    }*/
}); 

// Mobile menu toggle
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuToggle && mobileMenu) {
    mobileMenuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('active');
    });
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    if (mobileMenu && mobileMenuToggle && mobileMenu.classList.contains('active')) {
        if (!mobileMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
            mobileMenu.classList.remove('active');
        }
    }
});

// Close mobile menu when a link is clicked
const mobileLinks = document.querySelectorAll('.mobile-nav-link');
mobileLinks.forEach(link => {
    link.addEventListener('click', function() {
        if (mobileMenu) mobileMenu.classList.remove('active');
    });
});


