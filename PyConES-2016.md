# Aprendiendo magia negra con Python, optimización estocástica y simuladores 

## Breve descripción

La optimización mediante algoritmos estocásticos —ej. algoritmos genéticos o por enjambre de partículas— presenta una serie de ventajas frente a los algoritmos _«clásicos»_ deterministas al no requerir el cálculo de las derivadas del sistema por lo que su implementación en simuladores es casi inmediata. En esta charla se explicará mediante código las ventajas del algoritmo PSO (_Particle Swarm Optimization_) y se mostrarán ejemplos no triviales haciendo uso de simuladores de procesos químicos.

## Resumen detallado

La simulación y optimización de procesos han experimentado un crecimiento considerable durante los últimos años. Con el avance, abaratamiento de arquitecturas y mejora de software para procesamiento en paralelo, muchas industrias apuestan por algoritmos estocásticos para mejorar la producción, reducir los costes o disminuir el impacto medioambiental.


Debido a la complejidad de la multitud de procesos industriales, es habitual hacer uso de simuladores donde existe un flujo de datos con los que se opera en módulos o bloques de forma secuencial. Sin embargo, con respecto a la optimización, los simuladores no han alcanzado un grado de desarrollo o robustez deseada —no existe aún un botón mágico en los simuladores que “optimice”, por ejemplo, el número de equipos y/o las condiciones de operación—.


En esta charla, sin embargo, mostraremos con código Python como algoritmos del tipo PSO ([_Particle Swarm Optimization_](https://es.wikipedia.org/wiki/Optimizaci%C3%B3n_por_enjambre_de_part%C3%ADculas)) pueden ser acoplados fácilmente con simuladores de procesos para resolver problemas de optimización. Recientemente en Python han aparecido librerías especializadas en algoritmos [_libres de derivadas_](https://en.wikipedia.org/wiki/Derivative-free_optimization) ([OpenMDAO](https://en.wikipedia.org/wiki/OpenMDAO)-NASA, [PyGMO](http://esa.github.io/pygmo/)-ESA o [PySwarm](http://pythonhosted.org/pyswarm/), entre otras). Éstas, junto al uso de simuladores (propietarios o libres) pueden ser muy interesantes en un gran número de aplicaciones como herramientas de optimización de _~~magia~~ caja negra_.

Por ejemplo, en el ámbito de la ingeniería de procesos químicos, los [simuladores secuenciales modulares](https://en.wikipedia.org/wiki/List_of_chemical_process_simulators) (como Aspen Hysys, Aspen Plus, Pro/II, ChemCAD…) son ampliamente utilizados  para el diseño refinerías, plantas químicas y/o tratamiento de aguas. Estos paquetes de software incluyen bibliotecas termodinámicas y modelos numéricos que conducen a predicciones precisas de los procesos implementados. Por ello  y a modo de aplicación real, combinaremos finalmente estos simuladores con Python, lo que nos permitirá obtener un ahorro económico significativo en el diseño final de una planta de procesos químicos.

Esta charla será impartida por investigadores de ingeniería química de la Universidad de Alicante miembros de [CAChemE](http://cacheme.org/) y su estructura será la siguiente:
* Introducción a la problemática en la optimización matemática (5 min). Se realizará una introducción visual a conceptos de optimización determinista, así como a las ventajas e inconvenientes que presentan los algoritmos estocásticos.
* Implementación del algoritmo PSO (15 min). Se verán ejemplos sencillos de optimización con Python y se explicará de manera breve cómo acelerar su tiempo de ejecución. 
* Serie de ejemplos de problemas de optimización en ingeniería (10 min), con especial hincapié en ejemplos reales en la industria e ingeniería química.

## Por qué no deberías perderte esta charla
La charla podrá ser seguida tanto como por principiantes en el mundo de la ciencia e ingeniería así como por desarrolladores/as profesionales. Creemos que con esta charla captaremos la atención de estos dos espectros ya que:

1. Python es sencillo de leer y la implementación de estos algoritmos estocásticos puede ser entendida por gente sin experiencia en programación pero que hace uso de simuladores. 
2. Los desarrolladores/as podrán ver cómo sus conocimientos en procesamiento en paralelo y/o optimización de código con Python pueden darles nuevas aplicaciones en nichos de mercado quizás no tan conocidos. 
