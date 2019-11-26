# co-change-dependencies
Investigating whether co-change dependencies introduce bugs \\

Ao todo, teremos que analisar 39 projetos apache ("project_list.txt")\\

dockerhub (projectdraco/mining-cochange)\\

Cada linha corresponde a uma dependência, ou, em outras palavras, a uma aresta do grafo de dependência de co-change. Os campos do arquivo são separados por tab (\t), sendo que cada campo significa o seguinte:\\

1.  método/campo que representa o vértice de origem da aresta\\
2.  método/campo que representa o vértice de destino da aresta\\
3.  support count\\
4.  confidence\\
5.  ignore\\
6.  qtd total de commits\\
7.  hashes dos commits\\

Para definição de support count e confidence, sugiro que leia algum dos meus artigos sobre co-change. Por ser o [1]. No arquivo em anexo eu não determinei limiares para essas métricas, então você terá que filtrar de acordo com sua conveniência. Só para exemplificar, eu geralmente uso support count 2 e confidence 0.5, mas isso vai de acordo com a sua pesquisa.\\

Os passos  para gerar o arquivo foram de co-change:\\

1.  $ git clone https://github.com/apache/storm  \\
2.  $ mkdir storm-hr  \\
3.  $ cd storm-hr   \\
4.  $ git init --bare \\ 
5.  $ cd ..   \\
6.  $ docker run --rm -v $PWD/storm:/source -v $PWD/storm-hr:/dest projectdraco/g2h converter.sh /source /dest  # levou cerca de 3 horas \\
7.  $ cd storm-hr \\
8.  $ docker run -it --rm -v $PWD:/repo projectdraco/mining-cochange --output=rules-and-commits > storm-cochange.mdg # levou cerca de 1 hora \\

Passos para pegar todos os commits com as datas:\\

git log --pretty=format:%H,%cd  >  all_commits.csv\\

Os commits que induziram bugs estão em ("szz_phaseII.csv")
