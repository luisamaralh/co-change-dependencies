# co-change-dependencies
Investigating whether co-change dependencies introduce bugs <br />
Ao todo, teremos que analisar 39 projetos apache ("project_list.txt")<br />
dockerhub (projectdraco/mining-cochange)<br />

Cada linha corresponde a uma dependência, ou, em outras palavras, a uma aresta do grafo de dependência de co-change. Os campos do arquivo são separados por tab (\t), sendo que cada campo significa o seguinte:<br />

1.  método/campo que representa o vértice de origem da aresta<br />
2.  método/campo que representa o vértice de destino da aresta<br />
3.  support count<br />
4.  confidence<br />
5.  ignore<br />
6.  qtd total de commits<br />
7.  hashes dos commits<br />

Para definição de support count e confidence, sugiro que leia algum dos meus artigos sobre co-change. Por ser o [1]. No arquivo em anexo eu não determinei limiares para essas métricas, então você terá que filtrar de acordo com sua conveniência. Só para exemplificar, eu geralmente uso support count 2 e confidence 0.5, mas isso vai de acordo com a sua pesquisa.<br />

Os passos  para gerar o arquivo foram de co-change:<br />

1.  $ git clone https://github.com/apache/storm  <br />
2.  $ mkdir storm-hr  <br />
3.  $ cd storm-hr   <br />
4.  $ git init --bare <br /> 
5.  $ cd ..   <br />
6.  $ docker run --rm -v $PWD/storm:/source -v $PWD/storm-hr:/dest projectdraco/g2h converter.sh /source /dest  # levou cerca de 3 horas <br />
7.  $ cd storm-hr <br />
8.  $ docker run -it --rm -v $PWD:/repo projectdraco/mining-cochange --output=rules-and-commits > storm-cochange.mdg # levou cerca de 1 hora <br />

Passos para pegar todos os commits com as datas:<br />

git log --pretty=format:%H,%cd  >  all_commits.csv<br />

Os commits que induziram bugs estão em ("szz_phaseII.csv")
