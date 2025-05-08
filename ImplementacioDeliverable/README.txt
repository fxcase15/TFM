A continuació descriurem els fitxers que hem utilitzat per l'apartat de implementació:
1. urls.txt --> inclou tots els URLs que manualment vam extreure de la web de Albert Heijn amb el html de la web via "inspeccionar"
2. script.py --> es l'script que es va utilitzar per obtenir totes les dades necessaries dels productes de alimentació de la web de Albert Heijn
3. data.xlsx --> resultat del data scraping.
4. https://forms.gle/3qqZGsAXNtCRMgPA9 -->  link al forms creat 
5. AH Recommendation ML Model.yxmd (Alteryx primer MVP)  --> Primer MVP adjunt amb Alteryx  !!!cal llicencia per poder obrir i executar el workflow. Aquí ja tenim una versió del scoring model que ja funciona.
Els inputs aqui son les dades que fiquen els usuaris al forms. I el output és un fitxer amb un scoring per cada un dels productes calculat de forma matemàtica d'acord amb les preferències dels usuaris.
6. Normalizing_Product_Quantities.py --> Un cop realitzat el primer MVP vam mirar de normalitzar les quantitats per fer recomanacions per baixar de pes o poder tenir en compte les calories per quantitat en els calculs.
7. products_quantities_normalized.xlsx --> aquí obtenim un dataset netejat i complet, un cop processat amb Alteryx i normalitzat per quantitats
Nota: Fins aquí teniem el producte ja gairebé finalitzat, però teniem un problema, no haviem fet servir tècniques de ML per a predir el model i tampoc teniem dades massives de usuaris, per tant haviem de centrarnos amb dades que ja teniem per millorar el model.
Per tant, ens vam centrar amb millorar el Nutriscore (valor que indica com de saludable és un producte). Hi ha molts articles sense nutriscore i per tant utilitzem eines de ML per predir el nutriscore per els aliments que no en tenen.
8. prediccio_nutriscore_final_amb_MAE.ipynb --> estudi i analisis de machine learning amb 3 models diferents i un quart model combinant la resta de models, el qual ha resultat ser el més efficient. Exportem fitxer excel que despres importarem a products_quantities_normalized.xlsx
9. prediccio_nutriscore_final_amb_MAE.html --> output del ipynb anterior amb grafics indicant quin es el millor model
10. products_quantities_normalized_amb_ML.xlsx
11. app.py --> frontend amb Streamlit, el machinlearning ja ha estat importat a traves del fitxer products_quantities_normalized.xlsx millorat i amb Machine learning models.
12. link al producte final.txt --> fes click a "Yes, get this app back up!" per a iniciar de nou la instancia del servidor (tarda 1 minut) i llavors funciona el producte final
13. Video recomanador Articles AH.mp4 --> video demostratiu del MVP final
