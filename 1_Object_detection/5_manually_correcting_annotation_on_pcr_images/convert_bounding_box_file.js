const fs = require('fs');
const path = require('path');

const directoryPath = path.join(__dirname, 'final_pcr_images/pcrsalmo');
const classNumber = '3';

// Read the directory
fs.readdir(directoryPath, (err, files) => {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }

    // Filter out the .txt files
    const txtFiles = files.filter(file => path.extname(file) === '.txt');

    // Read, modify, and save each .txt file
    txtFiles.forEach(file => {
        const filePath = path.join(directoryPath, file);
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return console.log('Unable to read file: ' + err);
            }

            // Modify the content
            const modifiedData = data.split('\n').map(line => {
                if (line.trim() !== '') {
                    const parts = line.split(' ');
                    parts[0] = classNumber;
                    return parts.join(' ');
                }
                return line;
            }).join('\n');

            // Write the modified content back to the file
            fs.writeFile(filePath, modifiedData, 'utf8', err => {
                if (err) {
                    return console.log('Unable to write file: ' + err);
                }
                console.log(`Updated content of ${file}`);
            });
        });
    });
});
