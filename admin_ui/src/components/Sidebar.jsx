import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Box } from '@mui/material';
import InventoryIcon from '@mui/icons-material/Inventory';
import SettingsIcon from '@mui/icons-material/Settings';
import StorageIcon from '@mui/icons-material/Storage';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { NavLink } from 'react-router-dom';

const drawerWidth = 220;

const navItems = [
  { text: 'Asset Inventory', icon: <InventoryIcon />, path: '/assets' },
  { text: 'ML Model Status', icon: <AssessmentIcon />, path: '/ml-models' },
  { text: 'Data Ingestion', icon: <StorageIcon />, path: '/data-ingestion' },
  { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
];

export default function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box', bgcolor: '#212b36', color: '#fff' },
      }}
    >
      <Toolbar />
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {navItems.map(({ text, icon, path }) => (
            <ListItem
              button
              key={text}
              component={NavLink}
              to={path}
              sx={{
                '&.active': { bgcolor: '#1a2027' },
                color: '#fff',
              }}
            >
              <ListItemIcon sx={{ color: '#fff' }}>{icon}</ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
} 