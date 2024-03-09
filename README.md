# 💎 Etimo Diamonds 2

## Algoritma Greedy

Algoritma Greedy adalah algoritma yang digunakan untuk memecahkan permasalahan secara langkah per langkah sedemikian sehingga pada setiap langkahnya memilih pilihan yang terbaik yang dapat diperoleh saat itu tanpa memperhatikan konsekuensi kedepannya dengan harapan pilihan tersebut akan mengantarkan kita pada solusi optimal global. Pada algoritma greedy, setiap pilihan yang telah diambil tidak dapat diubah pada langkah selanjutnya.

Pada permainan ini, Kami menggunakan algoritma greedy gradien. Kita membuat sebuah fungsi dalam bentuk dua dimensi yang menerima posisi koordinat x dan y serta seluruh state atau nilai dari permainan yang berupa Game Object seperti diamond ataupun player lain. Apabila kita membuat sebuah grafik pada koordinat 2D, akan terbentuk sebuah lembah. Lembah yang paling dalam memiliki arti sebuah koordinat dimana diamond akan terkumpul. kita tidak perlu menghitung nilai fungsi pada seluruh papan, namun hanya perlu empat koordinat yang dapat dituju oleh bot saat ini, ditambah satu posisi koordinat bot.

Alasan kami menggunakan startegi ini adalah : 
1. Bot akan bergerak ke area dengan konsentrasi diamond tertinggi yang jaraknya paling dekat dan memprioritaskan pengambilan diamond dengan poin tertinggi yang dapat ditampung oleh bot (diamond merah).
2. Selama perjalanan ke area dengan konsentrasi diamond banyak, jika ada diamond yang dekat maka bot juga akan mengambil diamond itu.
3. Bot akan cenderung kembali ke base saat waktu tersisa 10 detik sehingga bot akan mengamankan diamond yang ada di inventory daripada harus mengambil diamond dan tidak ada waktu untuk kembali ke base.
4. Bot memiliki mekanisme kembali ke base yang cukup baik sehingga dapat meminimalisasi kehilangan poin.


## How to Run 💻

1. To run one bot
    ```
    cd src
    ```
    ```
    python main.py --logic Gradient --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

2. To run multiple bots simultaneously

    For Windows
    ```
    cd src
    ```
    ```
    ./run-bots.bat
    ```

    For Linux / (possibly) macOS
    ```
    cd src
    ```
    ```
    ./run-bots.sh
    ```

    <b>Before executing the script, make sure to change the permission of the shell script to enable executing the script (for linux/macOS)</b>

    ```
    chmod +x run-bots.sh
    ```

#### Note:

-   If you run multiple bots, make sure each emails and names are unique
-   The email could be anything as long as it follows a correct email syntax
-   The name, and password could be anything without any space

## Author
1. Keanu Amadius Gonza Wrahatno  (13522082@mahasiswa.itb.ac.id)
2. Muhammad Atpur Rafif  (13522086@mahasiswa.itb.ac.id)
3. Muhamad Rafli Rasyiidin  (13522088@mahasiswa.itb.ac.id)


## Credits 🪙

This repository is adapted from https://github.com/Etimo/diamonds2

Some code in this repository is adjusted to fix some issues in the original repository and to adapt to the requirements of Algorithm Strategies course (IF2211), Informatics Undergraduate Program, ITB.

©️ All rights and credits reserved to [Etimo](https://github.com/Etimo)
