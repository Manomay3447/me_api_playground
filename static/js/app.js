// API base URL
const API_BASE = '';

// DOM elements
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const profileDisplay = document.getElementById('profile-display');
const apiResponse = document.getElementById('api-response');
const refreshButton = document.getElementById('refresh-profile');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupTabs();
    loadProfile();
    setupEventListeners();
});

// Tab functionality
function setupTabs() {
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Remove active class from all tabs and contents
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and content
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

// Event listeners
function setupEventListeners() {
    refreshButton.addEventListener('click', loadProfile);
}

// Load and display profile
async function loadProfile() {
    try {
        profileDisplay.innerHTML = '<div class="loading">Loading profile...</div>';
        
        const response = await fetch(`${API_BASE}/api/profile`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const profile = await response.json();
        displayProfile(profile);
    } catch (error) {
        console.error('Error loading profile:', error);
        profileDisplay.innerHTML = `
            <div class="error-message">
                <strong>Error:</strong> Failed to load profile. ${error.message}
            </div>
        `;
    }
}

function displayProfile(profile) {
    const profileHtml = `
        <div class="profile-info">
            <h3><i class="fas fa-user"></i> Personal Information</h3>
            <div class="info-item">
                <i class="fas fa-user-circle"></i>
                <strong>Name:</strong> ${profile.name || 'Not specified'}
            </div>
            <div class="info-item">
                <i class="fas fa-envelope"></i>
                <strong>Email:</strong> ${profile.email || 'Not specified'}
            </div>
            <div class="info-item">
                <i class="fas fa-graduation-cap"></i>
                <strong>Education:</strong> ${profile.education || 'Not specified'}
            </div>
        </div>

        <div class="profile-info">
            <h3><i class="fas fa-code"></i> Skills</h3>
            <div class="skills-grid">
                ${profile.skills && profile.skills.length > 0 
                    ? profile.skills.map(skill => `
                        <span class="skill-tag" style="animation-delay: ${Math.random() * 0.5}s">
                            ${skill.name} (${skill.level})
                        </span>
                    `).join('')
                    : '<p>No skills added yet.</p>'
                }
            </div>
        </div>

        <div class="profile-info">
            <h3><i class="fas fa-project-diagram"></i> Projects</h3>
            <div class="projects-grid">
                ${profile.projects && profile.projects.length > 0
                    ? profile.projects.map(project => `
                        <div class="project-card">
                            <h4>${project.title}</h4>
                            <p>${project.description || 'No description available.'}</p>
                            <div class="skills-grid" style="margin-top: 10px;">
                                ${project.technologies ? project.technologies.map(tech => 
                                    `<span class="skill-tag" style="background: #28a745;">${tech}</span>`
                                ).join('') : ''}
                            </div>
                            <div class="project-links">
                                ${project.links?.github ? `<a href="${project.links.github}" target="_blank"><i class="fab fa-github"></i> GitHub</a>` : ''}
                                ${project.links?.demo ? `<a href="${project.links.demo}" target="_blank"><i class="fas fa-external-link-alt"></i> Demo</a>` : ''}
                            </div>
                        </div>
                    `).join('')
                    : '<p>No projects added yet.</p>'
                }
            </div>
        </div>

        <div class="profile-info">
            <h3><i class="fas fa-briefcase"></i> Work Experience</h3>
            <div class="work-timeline">
                ${profile.work && profile.work.length > 0
                    ? profile.work.map(work => `
                        <div class="work-item ${work.is_current ? 'current' : ''}">
                            <h4>${work.position}</h4>
                            <div class="company">${work.company}</div>
                            <p>${work.description || 'No description available.'}</p>
                            <small style="color: #666;">
                                ${work.start_date ? formatDate(work.start_date) : 'Start date not specified'} - 
                                ${work.is_current ? 'Present' : (work.end_date ? formatDate(work.end_date) : 'End date not specified')}
                            </small>
                        </div>
                    `).join('')
                    : '<p>No work experience added yet.</p>'
                }
            </div>
        </div>

        <div class="profile-info">
            <h3><i class="fas fa-link"></i> Links</h3>
            <div class="social-links">
                ${profile.links?.github ? `<a href="${profile.links.github}" target="_blank" class="social-link"><i class="fab fa-github"></i> GitHub</a>` : ''}
                ${profile.links?.linkedin ? `<a href="${profile.links.linkedin}" target="_blank" class="social-link"><i class="fab fa-linkedin"></i> LinkedIn</a>` : ''}
                ${profile.links?.portfolio ? `<a href="${profile.links.portfolio}" target="_blank" class="social-link"><i class="fas fa-globe"></i> Portfolio</a>` : ''}
            </div>
            ${(!profile.links?.github && !profile.links?.linkedin && !profile.links?.portfolio) ? '<p>No links added yet.</p>' : ''}
        </div>
    `;
    
    profileDisplay.innerHTML = profileHtml;
}

// API testing functions
async function testEndpoint(method, endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        displayApiResponse({
            status: response.status,
            statusText: response.statusText,
            data: data
        });
    } catch (error) {
        displayApiResponse({
            error: error.message
        });
    }
}

async function testProjectsEndpoint() {
    const skillFilter = document.getElementById('skill-filter').value.trim();
    let url = '/api/projects';
    
    if (skillFilter) {
        url += `?skill=${encodeURIComponent(skillFilter)}`;
    }
    
    await testEndpoint('GET', url);
}

async function testSearchEndpoint() {
    const query = document.getElementById('search-query').value.trim();
    
    if (!query) {
        displayApiResponse({
            error: 'Please enter a search query'
        });
        return;
    }
    
    await testEndpoint('GET', `/api/search?q=${encodeURIComponent(query)}`);
}

function displayApiResponse(response) {
    apiResponse.textContent = JSON.stringify(response, null, 2);
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Add some smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add loading states to buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;
    
    return () => {
        button.textContent = originalText;
        button.disabled = false;
    };
}

// Enhanced error handling
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    // You could show a user-friendly error message here
});
