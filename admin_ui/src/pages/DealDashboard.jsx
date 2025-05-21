import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, TextField, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

function DealDashboard() {
  const [deals, setDeals] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchDeals = async () => {
    setLoading(true);
    const res = await fetch('/api/structuring/deals/');
    const data = await res.json();
    setDeals(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchDeals();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await fetch('/api/structuring/deals/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    });
    setName('');
    setDescription('');
    fetchDeals();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Deals</Typography>
      <Paper sx={{ p: 2, mb: 3 }}>
        <form onSubmit={handleCreate} style={{ display: 'flex', gap: 16 }}>
          <TextField label="Name" value={name} onChange={e => setName(e.target.value)} required />
          <TextField label="Description" value={description} onChange={e => setDescription(e.target.value)} />
          <Button type="submit" variant="contained">Add Deal</Button>
        </form>
      </Paper>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {deals.map((deal) => (
              <TableRow key={deal.id}>
                <TableCell>{deal.id}</TableCell>
                <TableCell>{deal.name}</TableCell>
                <TableCell>{deal.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default DealDashboard; 