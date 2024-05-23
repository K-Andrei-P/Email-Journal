#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Arguments Checking
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "rb");

    // Check not null
    if (file == NULL)
    {
        printf("Couldn't open file: \nExit code 1\n");
        return 1;
    }

    // Buffer
    uint8_t buffer[512];

    // Checking booleans
    bool fileOpened = false;
    FILE *jpeg;
    int fileNum = 0;
    char fileName[9];

    while(fread(buffer, 1, 512, file) == 512)
    {
        // Opening Sequence for 1st search
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 && !fileOpened)
        {
            fileNum++;
            sprintf(fileName, "%03i.jpeg", fileNum);

            jpeg = fopen(fileName, "w");
            fwrite(buffer, 1, 512, jpeg);
            fileOpened = true;
        } else if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 && fileOpened)
        {
            // Coming across a Block that is the start of a new image
            // Close last jpeg file
            fclose(jpeg);
            // Assign jpeg file to new name
            fileNum++;
            sprintf(fileName, "%03i.jpeg", fileNum);
            jpeg = fopen(fileName, "w");
            fwrite(buffer, 1, 512, jpeg);

        } else if (fileOpened)
        {
            // If not the start of a imag but image has already been opened
            jpeg = fopen(fileName, "a");
            fwrite(buffer, 1, 512, jpeg);
        }
    }
    if (fileOpened) {
        fileOpened = false;
        fclose(jpeg);
        return 0;
    }
}
