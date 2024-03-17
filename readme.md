# Project Harvester

Project Harvester is a program created to control Linux systems remotely by uploading videos to Youtube.

The program monitors a Youtube channel until a video is uploaded, decodes the QR code from the thumbnail of the uploaded video and executes a command. The QR codes in the videos can use cleartext or AES-encrypted values.


![img1](./images/expl.png)

## Credit

The idea for this project was originally conceived by [Ricardo Ruiz](https://github.com/ricardojoserf). I have recreated his [project](https://github.com/ricardojoserf/SharpCovertTube) entirely from scratch with the aim of understanding how it works and adapting it for Linux systems.
