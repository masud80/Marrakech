import { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress, Alert, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, IconButton } from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';

export default function AssetInventory() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [form, setForm] = useState({ name: '', type: '', value: '', currency: '', description: '' });
  const [processing, setProcessing] = useState(false);

  const fetchAssets = () => {
    setLoading(true);
    fetch('/api/assets/')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch assets');
        return res.json();
      })
      .then(setAssets)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAssets();
  }, []);

  const handleOpenAdd = () => {
    setForm({ name: '', type: '', value: '', currency: '', description: '' });
    setAddOpen(true);
  };
  const handleOpenEdit = (asset) => {
    setSelectedAsset(asset);
    setForm({ ...asset });
    setEditOpen(true);
  };
  const handleOpenDelete = (asset) => {
    setSelectedAsset(asset);
    setDeleteOpen(true);
  };
  const handleClose = () => {
    setAddOpen(false);
    setEditOpen(false);
    setDeleteOpen(false);
    setSelectedAsset(null);
    setForm({ name: '', type: '', value: '', currency: '', description: '' });
    setProcessing(false);
  };

  const handleChange = (e) => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleAdd = () => {
    setProcessing(true);
    fetch('/api/assets/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, value: parseFloat(form.value) }),
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to add asset');
        return res.json();
      })
      .then(() => {
        fetchAssets();
        handleClose();
      })
      .catch(e => setError(e.message))
      .finally(() => setProcessing(false));
  };

  const handleEdit = () => {
    setProcessing(true);
    fetch(`/api/assets/${selectedAsset.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, value: parseFloat(form.value) }),
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to update asset');
        return res.json();
      })
      .then(() => {
        fetchAssets();
        handleClose();
      })
      .catch(e => setError(e.message))
      .finally(() => setProcessing(false));
  };

  const handleDelete = () => {
    setProcessing(true);
    fetch(`/api/assets/${selectedAsset.id}`, {
      method: 'DELETE',
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to delete asset');
        return res.json();
      })
      .then(() => {
        fetchAssets();
        handleClose();
      })
      .catch(e => setError(e.message))
      .finally(() => setProcessing(false));
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h4" gutterBottom>
          Asset Inventory
        </Typography>
        <Button variant="contained" startIcon={<Add />} onClick={handleOpenAdd} sx={{ mb: 2 }}>
          Add Asset
        </Button>
        {loading ? (
          <CircularProgress />
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Value</TableCell>
                  <TableCell>Currency</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {assets.map((asset) => (
                  <TableRow key={asset.id}>
                    <TableCell>{asset.id}</TableCell>
                    <TableCell>{asset.name}</TableCell>
                    <TableCell>{asset.type}</TableCell>
                    <TableCell>{asset.value}</TableCell>
                    <TableCell>{asset.currency}</TableCell>
                    <TableCell>{asset.description}</TableCell>
                    <TableCell>
                      <IconButton color="primary" onClick={() => handleOpenEdit(asset)}><Edit /></IconButton>
                      <IconButton color="error" onClick={() => handleOpenDelete(asset)}><Delete /></IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
        {/* Add Modal */}
        <Dialog open={addOpen} onClose={handleClose}>
          <DialogTitle>Add Asset</DialogTitle>
          <DialogContent>
            <TextField margin="dense" label="Name" name="name" value={form.name} onChange={handleChange} fullWidth required />
            <TextField margin="dense" label="Type" name="type" value={form.type} onChange={handleChange} fullWidth required />
            <TextField margin="dense" label="Value" name="value" value={form.value} onChange={handleChange} type="number" fullWidth required />
            <TextField margin="dense" label="Currency" name="currency" value={form.currency} onChange={handleChange} fullWidth required />
            <TextField margin="dense" label="Description" name="description" value={form.description} onChange={handleChange} fullWidth />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleAdd} disabled={processing} variant="contained">Add</Button>
          </DialogActions>
        </Dialog>
        {/* Edit Modal */}
        <Dialog open={editOpen} onClose={handleClose}>
          <DialogTitle>Edit Asset</DialogTitle>
          <DialogContent>
            <TextField margin="dense" label="Name" name="name" value={form.name} onChange={handleChange} fullWidth required />
            <TextField margin="dense" label="Type" name="type" value={form.type} onChange={handleChange} fullWidth required />
            <TextField margin="dense" label="Value" name="value" value={form.value} onChange={handleChange} type="number" fullWidth required />
            <TextField margin="dense" label="Currency" name="currency" value={form.currency} onChange={handleChange} fullWidth required />
            <TextField margin="dense" label="Description" name="description" value={form.description} onChange={handleChange} fullWidth />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleEdit} disabled={processing} variant="contained">Save</Button>
          </DialogActions>
        </Dialog>
        {/* Delete Modal */}
        <Dialog open={deleteOpen} onClose={handleClose}>
          <DialogTitle>Delete Asset</DialogTitle>
          <DialogContent>
            <Typography>Are you sure you want to delete asset "{selectedAsset?.name}"?</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleDelete} disabled={processing} color="error" variant="contained">Delete</Button>
          </DialogActions>
        </Dialog>
      </CardContent>
    </Card>
  );
} 