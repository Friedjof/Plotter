# Der Python-Simulator - [Zum Blog Artikel](https://blog.noweck.info/der-plotter/)

Den Python-Simulator des Plotters habe ich vor allem deshalb gebaut, um meine theoretischen Berechnungen praktisch nachzuweisen zu können. Dies hat mir besonders geholfen noch einige Hürden zu erkennen. Die Grafik ist dabei bewusst relativ simpel gehalten. Für die Erstellung der Oberfläche habe ich die einfache Python Library Tkinter genutzt. Für die mathematischen Berechnungen habe ich die Standard-Library numpy hinzugezogen. Zentral sind die beiden Funktionen “position” und “angles”.


## Screenshot
![Plotter Simulation](/images/animations/Plotter-circles.gif)

Die Funktion Position kann anhand eines Punktes die fehlenden Punkte und Winkel des Pentagons berechnen. Die Rückgabe erfolgt als Pentagon-Objekt. Dabei wird auch die Tatsache berücksichtigt, dass nicht alle Punkte erreichbar sind und Selbstkollisionen ausgeschlossen werden können.

Die Funktion Angles kann durch die Übergabe der aktuellen Winkel an den beiden Motoren die genaue Position des Stiftes ermitteln. Daher stellt dies die Umkehrung der Funktion Position dar. Hierbei werden natürlich auch Winkel-Grenzen beachtet.
## Feedback

If you have any feedback, please reach out to us at git@noweck.info
## Authors

- [@friedjof](https://www.github.com/friedjof)

