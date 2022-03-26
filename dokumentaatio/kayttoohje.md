# Luolastogeneraattorin käyttöohje
Pääohjelma: src/main.py  
Saat seuraavat vaihtoehdot:  
1. uusi luolasto
  - Kysyy halutun leveyden ja korkeuden. Leveys on rajattu terminaalin leveyden takia
1. bsp rooms
  - Luo 7-12 huonetta. Ei tarjoa toistaiseksi mitään vaihtoehtoja. Tällä hetkellä näyttäisi aina täyttävän luolaston ennen onnistunutta huoneiden luontia. Kaatuu liian pienillä luolastoilla. Toistaiseksi ei luo käytäviä.
  ![](kuvat/kayttoohje/bsp.png)  
  (BSP)
1. drunkard's walk
  - Aloittaa satunnaisesta kohdasta, liikkuu satunnaisesti pääsuuntiin kunnes annettu elinikä on loppu, jolloin aloittaa uudesta kohdasta. Syntyy uudestaan kunnes annettu osuus luolastosta on kaivettu. 
  ![](kuvat/kayttoohje/drunkard.png)  
  (Drunkard's walk tavoitteena 30, ikä 100)
1. basic directional dungeon
  - Kaivaa käytävän x-akselin suunnassa mutkitellen ja käytävän leveyttä vaihdellen annettujen parametrien mukaan. Voi olla kiinnostavampi ajettuna pariin kertaan.
  ![](kuvat/kayttoohje/directed1.png)  
  (Basic directional dungeon mutkaisuus 50, vaihtelu 10)
  ![](kuvat/kayttoohje/directed2.png)
  (Algoritmi ajettu uudestaan samoilla parametreillä)
  ![](kuvat/kayttoohje/directed3.png)
  (Vielä kolmannen kerran)
