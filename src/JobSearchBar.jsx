import React, { useState } from "react";
import PdfUploader from "./PDFUploader.jsx";

function JobSearchForm({ darkMode }) {
  const [jobTitle, setJobTitle] = useState("");
  const [jobType, setJobType] = useState("");
  const [location, setLocation] = useState("");
  const [jobResults, setJobResults] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setJobResults([]); // Clear previous results

    const requestData = {
      job_title: jobTitle,
      job_type: jobType,
      location: location,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch job data");
      }

      const data = await response.json();
      if (data.jobs) {
        setJobResults(data.jobs);
      } else {
        console.error("No jobs found");
      }
    } catch (error) {
      console.error("Error fetching job data:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div
        style={{
          display: "flex",
          gap: "10px",
          padding: "20px",
          marginTop: "50px",
          backgroundColor: darkMode ? "#1f2937" : "#fff",
          borderRadius: "5px",
          boxShadow: darkMode
            ? "0 1px 3px rgba(255, 255, 255, 0.12), 0 1px 2px rgba(255, 255, 255, 0.24)"
            : "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)",
        }}
      >
        <select
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          style={{ padding: "10px", border: "1px solid #ccc", borderRadius: "4px", flex: "1" }}
        >
          <option value="">Job title, keywords, or company</option>
          <option value="Software Engineer">Software Engineer</option>
          <option value="Data Scientist">Data Scientist</option>
          <option value="Systems Administrator">Systems Administrator</option>
          <option value="Network Engineer">Network Engineer</option>
          <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
          <option value="DevOps Engineer">DevOps Engineer</option>
          <option value="Cloud Architect">Cloud Architect</option>
          <option value="Artificial Intelligence Engineer">Artificial Intelligence Engineer</option>
          <option value="Software Tester">Software Tester</option>
          <option value="Database Administrator">Database Administrator</option>
          <option value="App Developer">App Developer</option>
          <option value="UX/UI Designer">UX/UI Designer</option>
          <option value="Full Stack Developer">Full Stack Developer</option>
          <option value="Product Manager">Product Manager</option>
        </select>

        <select
          value={jobType}
          onChange={(e) => setJobType(e.target.value)}
          style={{ padding: "10px", border: "1px solid #ccc", borderRadius: "4px", flex: "0.5" }}
        >
          <option value="">Job Type</option>
          <option value="fulltime">Full-time</option>
          <option value="parttime">Part-time</option>
          <option value="internship">Internship</option>
        </select>

        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location (eg. Davis, CA)"
          style={{ padding: "10px", border: "1px solid #ccc", borderRadius: "4px", flex: "1" }}
        />

        <button
          type="submit"
          style={{
            padding: "10px 20px",
            backgroundColor: darkMode ? "#9F67E0" : "#4285f4",
            color: darkMode ? "#1E1B29" : "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Search
        </button>
      </div>

      {/* Display job results */}
      <div>
        {jobResults.length > 0 && (
        <div>
          <h3>Job Results</h3>
          <ul>
            {jobResults.map((job, index) => (
            <li key={index}>
              <strong>{job.title}</strong> at {job.company} - {job.location} <br />
              <strong>Match Percentage:</strong> {job.match_percentage}% <br />
              <a href={job.job_url} target="_blank" rel="noopener noreferrer">
                Apply Here
              </a>
            </li>
            ))}
          </ul>
        </div>
        )}
      </div>

      <div style={{ textAlign: "center", marginTop: "15px" }}>
        <button style={{ border: "none", background: "none", color: darkMode ? "#9F67E0" : "#4285f4", cursor: "pointer", fontSize: "11px" }}>
          <PdfUploader />
        </button>
      </div>
    </form>
  );
}

export default JobSearchForm;