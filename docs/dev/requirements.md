# Requirements Document

## Introduction

This project intention is help teachers, hack town leaders to create communities to envolve peoples and send activities and challenges to be evaluated and receive feedback's.

## Requisitos Funcionais

| ID    | Descrição                                                                                  | Complexidade | Importância | Dependência |
| ----- | ------------------------------------------------------------------------------------------ | ------------ | ----------- | ----------- |
| RF001 | O sistema deve permitir que pessoas se cadastrem                                           | Baixa        | Alta        |             |
| RF002 | O sistema deve permitir usuários manter uma sessão com o sistema                           | Média        | Alta        | RF001       | 
| RF003 | O sistema deve permitir que os usuários visualizem, alterem suas informações               | Média        | Alta        | RF002       |
| RF004 | O sistema deve permitir aos usuários manterem comunidades publicas ou privadas             | Média        | Alta        | RF002       | 
| RF005 | O sistema deve disponibilizar ao criador da comunidade manter novos administradores        | Média        | Alta        | RF004       | 
| RF006 | O sistema deve permitir que usuários entrem e visualizem suas comunidades                  | Baixa        | Alta        | RF004       |
| RF007 | O sistema deve disponilizar aos administradores a expulsão de membros                      | Baixa        | Alta        | RF005       |
| RF008 | O sistema deve permitir administradores de uma comunidade manter posts informativos        | Média        | Alta        | RF004       |
| RF009 | O sistema deve permitir membros de uma comunidade comentar em posts informativos           | Média        | Média       | RF008       |
| RF010 | O sistema deve permitir usuários adiconem um cometário com menção a outro cometário        | Média        | Baixa       | RF009       |
| RF011 | O sistema deve permitir aos administradores de uma comunidade a manter atividades          | Média        | Alta        | RF004       |
| RF012 | O sistema deve permitir que os membros de comunidades submetam um repositório Git as atividades | Alta    | Alta        | RF011       |
| RF013 | O sistema deve permitir que membro que submeteu-se a atividade e os administradores visualizem o repositório Git | Alta | Alta | RF012|
| RF014 | O sistema deve permitir aos administradores de uma comunidade avaliarem uma atividade      | Média        | Alta        | RF013       |
| RF015 | O sistema deve permitir aos membros de uma comunidade comentar em uma atividade            | Média        | Baixa       | RF011       |
| RF016 | O sistema deve permitir usuários descobrir novas comunidades através de categorias         | Média        | Alta        | RF004       |
| RF017 | O sistema deve permitir aos administradores de comunidades manterem anexos a posts e atividades | Alta    | Média       | RF011       | 
