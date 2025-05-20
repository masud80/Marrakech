import { useEffect, useState } from 'react';
import {
  Card, CardContent, Typography, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert, Box
} from '@mui/material';

export default function MLModelStatus() {
  const [models, setModels] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retraining, setRetraining] = useState(null);
  const [retrainOutput, setRetrainOutput] = useState({});

  useEffect(() => {
    fetch('/api/models')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch models');
        return res.json();
      })
      .then(data => {
        setModels(data);
        data.forEach(model => fetchMetrics(model.id));
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
    // eslint-disable-next-line
  }, []);

  const fetchMetrics = (modelId) => {
    fetch(`/api/models/${modelId}/metrics`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch metrics');
        return res.json();
      })
      .then(data => setMetrics(m => ({ ...m, [modelId]: data.metrics })))
      .catch(() => setMetrics(m => ({ ...m, [modelId]: 'N/A' })));
  };

  const handleRetrain = (modelId) => {
    setRetraining(modelId);
    setError(null);
    fetch(`/api/models/${modelId}/retrain`, { method: 'POST' })
      .then(res => {
        if (!res.ok) throw new Error('Retrain failed');
        return res.json();
      })
      .then(data => {
        setRetrainOutput(o => ({ ...o, [modelId]: data.output }));
        fetchMetrics(modelId);
      })
      .catch(e => setError(e.message))
      .finally(() => setRetraining(null));
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h4" gutterBottom>ML Model Status</Typography>
        {error && <Alert severity="error">{error}</Alert>}
        {loading ? <CircularProgress /> : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Model ID</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Metrics</TableCell>
                  <TableCell>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {models.map(model => (
                  <TableRow key={model.id}>
                    <TableCell>{model.id}</TableCell>
                    <TableCell>{model.name}</TableCell>
                    <TableCell>{metrics[model.id] || <CircularProgress size={16} />}</TableCell>
                    <TableCell>
                      <Button
                        variant="outlined"
                        size="small"
                        onClick={() => handleRetrain(model.id)}
                        disabled={retraining === model.id}
                      >
                        {retraining === model.id ? <CircularProgress size={16} /> : 'Retrain'}
                      </Button>
                      {retrainOutput[model.id] && (
                        <Box mt={1}>
                          <Typography variant="body2" color="textSecondary">
                            Retrain Output:<br />
                            <pre style={{ margin: 0 }}>{retrainOutput[model.id]}</pre>
                          </Typography>
                        </Box>
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