# Image-Processing
## Project 1: Braille-Translator
Braille is a system of raised dots that can be read by touch and is used by visually impaired people to read and write. Converting an image of Braille to text can be a time-consuming and error-prone task. However, a solution has been developed that can automate this process with high accuracy. This solution uses several image processing techniques, including Gaussian blur, thresholding, erosion, and connected component analysis (CCA), to detect and recognize individual Braille characters. A clustering algorithm is then applied to convert each character into a 6-character string, representing a Braille unit. Finally, post-processing steps, including key creation and enhancement, are used to ensure accurate translation. This solution has the potential to make digital information more accessible to visually impaired individuals and improve their quality of life. 

![image](https://github.com/ZakriyaParacha46/Image-Processing/assets/82748498/f711dfd0-a40c-4f90-b0e0-e97cfb4fb86d)
### Methodology
- Apply Gaussian blur to remove imperfections, black dots, and pixels from the input image.
- Convert the 8-bit gray image to binary to improve connectivity analysis.
- Erode the image to decrease the number of white pixels, causing black dots to spread out and join to form characters.
- Apply CCA8 function to the eroded image to obtain the number of characters, their statistics, and an object map with labeled connected objects.
- Convert each object into a 6-character string where each character represents a Braille unit.
- Post-processing steps, including key creation and enhancement, are used to ensure accurate translation.
- The final output is the converted Braille text.
- Use statistics to find the distance between consecutive objects and mark them as spaces if the difference is greater than the threshold.
- Add a bounding box around each object using its maximum length, width, and initial points to focus on one character at a time.
- Apply clustering algorithm to each character as a vertical rectangle, crop it in a 3x2 dimension, and check each part to determine if it represents a Braille unit or is white.

### Output:
The conversion table is a JSON file containing mappings between Braille characters and English letters. Each key is a 6-digit binary string representing a 3x2 Braille dot pattern, and each value is the corresponding English lowercase letter. The translate function uses this table to convert Braille characters in the chars array to text. 
Each Braille character is represented by a 3x2 grid of dots, where a dot can either be raised (1) or flat (0). The 6-digit binary strings in the conversion table represent the arrangement of these dots, where the first three digits correspond to the left column of the grid, and the last three digits correspond to the right column. 

![image](https://github.com/ZakriyaParacha46/Image-Processing/assets/82748498/9ea4f94e-f7d1-452e-ab30-2460b033f182)


Reference: [Project 1 Article](https://www.zakriyaparacha.com/projects/braille-language-translator)

