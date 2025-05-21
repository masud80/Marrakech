import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, TextField, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

function PortfolioDashboard() {
  const [portfolios, setPortfolios] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchPortfolios = async () => {
    setLoading(true);
    const res = await fetch('/api/investment/portfolios/');
    const data = await res.json();
    setPortfolios(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await fetch('/api/investment/portfolios/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    });
    setName('');
    setDescription('');
    fetchPortfolios();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Portfolios</Typography>
      <Paper sx={{ p: 2, mb: 3 }}>
        <form onSubmit={handleCreate} style={{ display: 'flex', gap: 16 }}>
          <TextField label="Name" value={name} onChange={e => setName(e.target.value)} required />
          <TextField label="Description" value={description} onChange={e => setDescription(e.target.value)} />
          <Button type="submit" variant="contained">Add Portfolio</Button>
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
            {portfolios.map((portfolio) => (
              <TableRow key={portfolio.id}>
                <TableCell>{portfolio.id}</TableCell>
                <TableCell>{portfolio.name}</TableCell>
                <TableCell>{portfolio.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default PortfolioDashboard; 