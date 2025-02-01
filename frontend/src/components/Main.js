import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Button, 
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert
} from '@mui/material';
import { Typography } from '@mui/material';
import ExpandMore from '@mui/icons-material/ExpandMore';
import ImageUpload from './ImageUpload';

function Main() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ingredients, setIngredients] = useState(null);
  const [nutritionInfo, setNutritionInfo] = useState(null);
  const [augmentedInfo, setAugmentedInfo] = useState(null);
  const [error, setError] = useState(null);

  const handleFileUpload = async (uploadedFile) => {
    setFile(uploadedFile);
    setImageUrl(URL.createObjectURL(uploadedFile));
    setLoading(true);
    setError(null);

    try {
      // API calls would go here
      // const encodedImage = await encode_image(uploadedFile);
      // const ingredientsResult = await agent1_food_image_caption(encodedImage);
      // ... other API calls
    } catch (err) {
      setError('An error occurred while processing the image.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        🍎 Food AI
      </Typography>

      <Typography variant="body1" gutterBottom align="center">
        Analyze your food and get detailed nutritional insights! 🎉
      </Typography>

      <Box sx={{ my: 4 }}>
        <Typography variant="h5" gutterBottom>
          📸 Upload a Food Image
        </Typography>
        
        <ImageUpload onFileSelect={handleFileUpload} />

        {!file && (
          <Alert severity="info" sx={{ mt: 2 }}>
            Please upload a JPG, PNG, or JPEG image of your food to get started!
          </Alert>
        )}

        {imageUrl && (
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <img 
              src={imageUrl} 
              alt="Uploaded food" 
              style={{ maxWidth: '100%', borderRadius: '8px' }}
            />
          </Box>
        )}

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <CircularProgress />
          </Box>
        )}

        {ingredients && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              🍴 Extracted Food Ingredients
            </Typography>
            <Paper sx={{ p: 2 }}>
              {ingredients.map((ingredient, index) => (
                <Typography key={index}>{ingredient}</Typography>
              ))}
            </Paper>
          </Box>
        )}

        {nutritionInfo && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              🍽️ Nutrition Facts (per 100g)
            </Typography>
            <TableContainer component={Paper}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Ingredient</TableCell>
                    <TableCell>Carbs (g)</TableCell>
                    <TableCell>Energy (kcal)</TableCell>
                    <TableCell>Protein (g)</TableCell>
                    <TableCell>Fat (g)</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {/* Map through nutrition data */}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {augmentedInfo && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              🌟 Augmented Nutrition Information
            </Typography>
            <Paper sx={{ p: 2 }}>
              <Typography>{augmentedInfo}</Typography>
            </Paper>
          </Box>
        )}

        <Accordion sx={{ mt: 4 }}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">📚 Source Information</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              The nutritional facts displayed above are sourced from the <strong>USDA SRLegacy Database</strong>. 
              Our system identifies the most similar food descriptions in the database based on the ingredients we identified. 
              While we strive to make the matches as accurate as possible, they might not always perfectly reflect the exact nutrition of your specific ingredient.
            </Typography>
          </AccordionDetails>
        </Accordion>
      </Box>
    </Container>
  );
}

export default Main;
