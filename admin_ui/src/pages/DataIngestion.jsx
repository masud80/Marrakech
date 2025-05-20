import { useState, useEffect } from 'react';
import {
  Card, CardContent, Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert, Box, Input
} from '@mui/material';

export default function DataIngestion() {
  const [file, setFile] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [triggering, setTriggering] = useState(null);

  const fetchJobs = () => {
    setLoading(true);
    fetch('/api/ingestion/jobs')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch jobs');
        return res.json();
      })
      .then(setJobs)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!file) return;
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);
    fetch('/api/ingestion/upload', {
      method: 'POST',
      body: formData,
    })
      .then(res => {
        if (!res.ok) throw new Error('Upload failed');
        return res.json();
      })
      .then(() => {
        setFile(null);
        fetchJobs();
      })
      .catch(e => setError(e.message))
      .finally(() => setUploading(false));
  };

  const handleTrigger = (jobId) => {
    setTriggering(jobId);
    setError(null);
    fetch('/api/ingestion/trigger', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_id: jobId }),
    })
      .then(res => {
        if (!res.ok) throw new Error('Trigger failed');
        return res.json();
      })
      .then(() => fetchJobs())
      .catch(e => setError(e.message))
      .finally(() => setTriggering(null));
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h4" gutterBottom>Data Ingestion</Typography>
        <Box mb={2}>
          <Input type="file" onChange={handleFileChange} inputProps={{ accept: '.csv' }} />
          <Button variant="contained" onClick={handleUpload} disabled={!file || uploading} sx={{ ml: 2 }}>
            {uploading ? <CircularProgress size={20} /> : 'Upload CSV'}
          </Button>
        </Box>
        {error && <Alert severity="error">{error}</Alert>}
        {loading ? <CircularProgress /> : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Job ID</TableCell>
                  <TableCell>Filename</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {jobs.map(job => (
                  <TableRow key={job.id}>
                    <TableCell>{job.id}</TableCell>
                    <TableCell>{job.filename}</TableCell>
                    <TableCell>{job.status}</TableCell>
                    <TableCell>
                      {job.status === 'uploaded' && (
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => handleTrigger(job.id)}
                          disabled={triggering === job.id}
                        >
                          {triggering === job.id ? <CircularProgress size={16} /> : 'Trigger Ingestion'}
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </CardContent>
    </Card>
  );
} 