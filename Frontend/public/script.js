
const jobs = [
    {
      title: "Software Engineer",
      company: "Tech Corp Inc.",
      location: "San Francisco, CA",
      salary: 110000,
      companyType: "corporate",
      remote: "no",
    },
    {
      title: "Data Scientist",
      company: "DataWorks LLC",
      location: "Remote",
      salary: 120000,
      companyType: "startup",
      remote: "yes",
    },
    {
      title: "Product Manager",
      company: "Innovate Solutions",
      location: "New York, NY",
      salary: 130000,
      companyType: "corporate",
      remote: "no",
    },
    {
      title: "UX Designer",
      company: "Creative Minds",
      location: "Remote",
      salary: 90000,
      companyType: "startup",
      remote: "yes",
    },
    {
      title: "computer engineer",
      company: "viit",
      location: "pune",
      salary: 90000,
      companyType: "startup",
      remote: "yes",
    },
    {
      title: "web developer",
      company: "viit",
      location: "pune",
      salary: 7000,
      companyType: "startup",
      remote: "yes",
    },
  ];
  
  // Function to render job cards
  function renderJobs(filteredJobs) {
    const jobsGrid = document.querySelector(".jobs-grid");
    jobsGrid.innerHTML = ""; // Clear existing job cards
  
    filteredJobs.forEach((job) => {
      const jobCard = document.createElement("div");
      jobCard.classList.add("job-card");
      jobCard.innerHTML = `
        <h4>${job.title}</h4>
        <p class="company">${job.company}</p>
        <p class="location">${job.location}</p>
        <p class="salary">$${job.salary.toLocaleString()}</p>
        <button class="btn btn-apply">Apply Now</button>
      `;
      jobsGrid.appendChild(jobCard);
    });
  }
  
  // Function to filter jobs
  function filterJobs() {
    const salaryRange = document.getElementById("salary-range").value;
    const location = document.getElementById("location").value.toLowerCase();
    const companyType = document.getElementById("company-type").value;
    const remoteWork = document.getElementById("remote-work").value;
  
    const filteredJobs = jobs.filter((job) => {
      // Filter by salary range
      if (salaryRange !== "all") {
        const [min, max] = salaryRange.split("-");
        if (max === "+") {
          if (job.salary < parseInt(min)) return false;
        } else {
          if (job.salary < parseInt(min) || job.salary > parseInt(max)) return false;
        }
      }
  
      // Filter by location
      if (location && !job.location.toLowerCase().includes(location)) return false;
  
      // Filter by company type
      if (companyType !== "all" && job.companyType !== companyType) return false;
  
      // Filter by remote work
      if (remoteWork !== "all" && job.remote !== remoteWork) return false;
  
      return true;
    });
  
    renderJobs(filteredJobs);
  }
  
  // Initial render of all jobs
  renderJobs(jobs);
  
  // Add event listener to Apply Filters button
  document.querySelector(".btn-apply-filters").addEventListener("click", filterJobs);