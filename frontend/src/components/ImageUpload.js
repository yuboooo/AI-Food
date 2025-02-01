import React from 'react';
import { Button, Box } from '@mui/material';
import CloudUpload from '@mui/icons-material/CloudUpload';

function ImageUpload({ onFileSelect }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
      onFileSelect(file);
    }
  };

  return (
    <Box sx={{ textAlign: 'center' }}>
      <input
        accept="image/*"
        style={{ display: 'none' }}
        id="raised-button-file"
        type="file"
        onChange={handleFileChange}
      />
      <label htmlFor="raised-button-file">
        <Button
          variant="contained"
          component="span"
          startIcon={<CloudUpload />}
        >
          Upload Image
        </Button>
      </label>
    </Box>
  );
}

export default ImageUpload;