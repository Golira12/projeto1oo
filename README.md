 <div>
        <h1>Jogo de Adivinhação: Casos de Uso</h1>
        <p>Este documento detalha os casos de uso textuais (formato completo e abstrato) para o jogo "Adivinhe o Número".</p>
        <h2>Caso de Uso: Iniciar Jogo</h2>
        <ul>
            <li><strong>Objetivo</strong>: Este caso de uso possibilita ao jogador iniciar uma nova sessão do jogo "Adivinhe o Número".</li>
            <li><strong>Ator</strong>: Jogador</li>
            <li><strong>Pré-Condições</strong>: Nenhuma (o aplicativo pode ser iniciado a qualquer momento).</li>
            <li><strong>Condição de Entrada</strong>: O ator <strong>Jogador</strong> executa o aplicativo do jogo.</li>
            <li><strong>Fluxo Principal</strong>:
                <ol>
                    <li>O sistema exibe a tela inicial com os campos "Nome do Herói" e "Grana Inicial".</li>
                    <li>O <strong>Jogador</strong> fornece seu nome no campo "Nome do Herói".</li>
                    <li>O <strong>Jogador</strong> fornece um valor numérico para o saldo inicial no campo "Grana Inicial".</li>
                    <li>O <strong>Jogador</strong> escolhe a opção "<strong>Iniciar Jogo (e a aventura!)</strong>".</li>
                    <li>O sistema valida o nome (não vazio) e o saldo inicial (numérico e não negativo).</li>
                    <li>O sistema cria uma instância do objeto <strong>Jogador</strong> com o nome e saldo fornecidos.</li>
                    <li>O sistema oculta os <em>widgets</em> de início de jogo e exibe os <em>widgets</em> da tela de apostas.</li>
                    <li>O sistema exibe uma mensagem de boas-vindas na interface (ex: "Bem-vindo(a), [Nome do Jogador]!").</li>
                    <li>O caso de uso se encerra.</li>
                </ol>
            </li>
            <li><strong>Fluxos Alternativos</strong>:
                <ul>
                    <li><strong>A1: Dados Inválidos de Entrada</strong>
                        <ul>
                            <li>Se o nome for vazio, ou o saldo inicial for não numérico ou negativo.</li>
                            <li>O sistema exibe uma mensagem de erro na interface (ex: "Erro: Nome ou saldo inválido. Não me venha com gracinha!" ou "Erro: Saldo inválido. É número, colega!").</li>
                            <li>O caso de uso retorna ao passo 1 do Fluxo Principal, permitindo que o <strong>Jogador</strong> tente novamente.</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
        <h2>Caso de Uso: Fazer Aposta</h2>
        <ul>
            <li><strong>Objetivo</strong>: Este caso de uso possibilita ao jogador realizar uma aposta em uma rodada do jogo.</li>
            <li><strong>Ator</strong>: Jogador</li>
            <li><strong>Pré-Condições</strong>:
                <ul>
                    <li>O <strong>Jogador</strong> já foi criado e inicializado no sistema.</li>
                    <li>O <strong>Jogador</strong> possui saldo disponível (saldo &gt; 0).</li>
                    <li>A tela de jogo está ativa.</li>
                </ul>
            </li>
            <li><strong>Condição de Entrada</strong>: O ator <strong>Jogador</strong> decide fazer uma aposta e insere os dados nos campos correspondentes.</li>
            <li><strong>Fluxo Principal</strong>:
                <ol>
                    <li>O sistema exibe o saldo atual do <strong>Jogador</strong> na interface.</li>
                    <li>O <strong>Jogador</strong> fornece um valor numérico para a aposta no campo "Quanto na roleta? (Corajoso(a)!)".</li>
                    <li>O <strong>Jogador</strong> fornece um número inteiro como palpite (entre MIN_NUMERO e MAX_NUMERO) no campo "Seu Palpite (1-10)".</li>
                    <li>O <strong>Jogador</strong> escolhe a opção "<strong>Mandar Ver! (Apostar)</strong>".</li>
                    <li>O sistema valida o valor da aposta (positivo e menor ou igual ao saldo disponível) e o palpite (dentro do intervalo 1-10 e numérico).</li>
                    <li>O sistema cria uma instância do objeto <strong>Aposta</strong> com o valor e palpite fornecidos.</li>
                    <li>O sistema gera um <code>numero_secreto</code> aleatório.</li>
                    <li>O sistema processa a <strong>Aposta</strong> comparando o palpite com o <code>numero_secreto</code>.</li>
                    <li>O sistema atualiza o saldo do <strong>Jogador</strong> (deposita o ganho ou saca a perda).</li>
                    <li>O sistema adiciona a <strong>Aposta</strong> ao <code>historico_apostas</code> do jogo.</li>
                    <li>O sistema exibe o resultado da aposta (se ganhou/perdeu, qual era o número secreto e o valor alterado) na interface.</li>
                    <li>O sistema atualiza o saldo exibido na interface.</li>
                    <li>O caso de uso se encerra.</li>
                </ol>
            </li>
            <li><strong>Fluxos Alternativos</strong>:
                <ul>
                    <li><strong>A1: Valor de Aposta Inválido</strong>
                        <ul>
                            <li>Se o valor da aposta fornecido for negativo, zero ou exceder o saldo do <strong>Jogador</strong>.</li>
                            <li>O sistema exibe uma mensagem de erro na interface (ex: "Aposta inválida. Saldo insuficiente ou valor errado!").</li>
                            <li>O caso de uso se encerra, esperando uma nova interação do <strong>Jogador</strong>.</li>
                        </ul>
                    </li>
                    <li><strong>A2: Palpite Inválido</strong>
                        <ul>
                            <li>Se o palpite fornecido for não numérico, não inteiro ou fora do intervalo MIN_NUMERO-MAX_NUMERO.</li>
                            <li>O sistema exibe uma mensagem de erro na interface (ex: "Palpite fora do intervalo. Concentra!").</li>
                            <li>O caso de uso se encerra, esperando uma nova interação do <strong>Jogador</strong>.</li>
                        </ul>
                    </li>
                    <li><strong>A3: Saldo Insuficiente para Continuar</strong>
                        <ul>
                            <li>Se após uma aposta (Fluxo Principal passo 9), o saldo do <strong>Jogador</strong> for igual ou inferior a zero.</li>
                            <li>O sistema exibe uma mensagem de "Game Over" na interface (ex: "Game Over! Seu saldo acabou. Fim de jogo.").</li>
                            <li>O sistema desativa a capacidade de fazer novas apostas (reinicia o estado do jogo para "não iniciado").</li>
                            <li>O caso de uso se encerra.</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
        <h2>Caso de Uso: Visualizar Histórico de Apostas</h2>
        <ul>
            <li><strong>Objetivo</strong>: Este caso de uso permite ao jogador consultar as últimas apostas realizadas.</li>
            <li><strong>Ator</strong>: Jogador</li>
            <li><strong>Pré-Condições</strong>: O jogo foi iniciado.</li>
            <li><strong>Condição de Entrada</strong>: O ator <strong>Jogador</strong> escolhe a opção "<strong>Ver meu passado (Histórico)</strong>".</li>
            <li><strong>Fluxo Principal</strong>:
                <ol>
                    <li>O sistema verifica se o <code>historico_apostas</code> possui registros.</li>
                    <li>O sistema formata as informações das últimas 5 Apostas (ou todas, se menos de 5) em uma string.</li>
                    <li>O sistema exibe essa string no campo de resultado da interface (ex: "Histórico Recente:\n[Lista de apostas]").</li>
                    <li>O caso de uso se encerra.</li>
                </ol>
            </li>
            <li><strong>Fluxos Alternativos</strong>:
                <ul>
                    <li><strong>A1: Histórico Vazio</strong>
                        <ul>
                            <li>Se o <code>historico_apostas</code> estiver vazio.</li>
                            <li>O sistema exibe a mensagem "Nada aqui. Vá apostar!" no campo de resultado.</li>
                            <li>O caso de uso se encerra.</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
        <h2>Caso de Uso: Atualizar Saldo na Interface</h2>
        <ul>
            <li><strong>Objetivo</strong>: Este caso de uso possibilita ao jogador ter uma visualização em tempo real do seu saldo atual.</li>
            <li><strong>Ator</strong>: Jogador (observador implícito)</li>
            <li><strong>Pré-Condições</strong>: O jogo está iniciado e o <strong>Jogador</strong> existe.</li>
            <li><strong>Condição de Entrada</strong>: Qualquer ação que altere o saldo do <strong>Jogador</strong> (iniciar jogo, fazer aposta, depositar).</li>
            <li><strong>Fluxo Principal</strong>:
                <ol>
                    <li>O sistema verifica o saldo atual do <strong>Jogador</strong>.</li>
                    <li>O sistema atualiza o texto do <em>widget</em> <code>saldo_label</code> na interface para exibir o valor mais recente do saldo.</li>
                    <li>O caso de uso se encerra.</li>
                </ol>
            </li>
        </ul>
        <h2>Caso de Uso: Depositar Dinheiro</h2>
        <ul>
            <li><strong>Objetivo</strong>: Este caso de uso permite ao jogador adicionar mais dinheiro ao seu saldo durante o jogo.</li>
            <li><strong>Ator</strong>: Jogador</li>
            <li><strong>Pré-Condições</strong>: O jogo está iniciado e o <strong>Jogador</strong> existe.</li>
            <li><strong>Condição de Entrada</strong>: O ator <strong>Jogador</strong> decide depositar dinheiro e insere o valor no campo correspondente.</li>
            <li><strong>Fluxo Principal</strong>:
                <ol>
                    <li>O sistema exibe o campo para "Valor a Depositar".</li>
                    <li>O <strong>Jogador</strong> fornece um valor numérico positivo para o depósito.</li>
                    <li>O sistema valida se o valor é positivo e numérico.</li>
                    <li>O sistema adiciona o valor fornecido ao saldo do <strong>Jogador</strong>.</li>
                    <li>O sistema exibe uma mensagem de sucesso na interface (ex: "Depósito de R$X realizado com sucesso!").</li>
                    <li>O sistema atualiza o saldo exibido na interface.</li>
                    <li>O caso de uso se encerra.</li>
                </ol>
            </li>
            <li><strong>Fluxos Alternativos</strong>:
                <ul>
                    <li><strong>A1: Valor de Depósito Inválido</strong>
                        <ul>
                            <li>Se o valor fornecido for negativo, zero ou não numérico.</li>
                            <li>O sistema exibe uma mensagem de erro na interface (ex: "Erro: Valor de depósito inválido. Digite um número válido.").</li>
                            <li>O caso de uso se encerra, esperando nova interação.</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
        <h2>Caso de Uso: Finalizar Jogo</h2>
        <ul>
            <li><strong>Objetivo</strong>: Este caso de uso possibilita ao jogador encerrar a sessão atual do jogo.</li>
            <li><strong>Ator</strong>: Jogador</li>
            <li><strong>Pré-Condições</strong>: O jogo está iniciado.</li>
            <li><strong>Condição de Entrada</strong>: O ator <strong>Jogador</strong> escolhe a opção para sair do jogo (ex: fechar a janela do aplicativo) ou seu saldo atinge zero.</li>
            <li><strong>Fluxo Principal</strong>:
                <ol>
                    <li>O sistema exibe o saldo final do <strong>Jogador</strong>.</li>
                    <li>O sistema exibe uma mensagem de despedida na interface (ex: "Jogo finalizado! Seu saldo final foi de R$X. Volte sempre!").</li>
                    <li>O sistema "reseta" o estado do jogo (define jogador como <code>None</code> e limpa o <code>historico_apostas</code>).</li>
                    <li>O sistema fecha o aplicativo.</li>
                    <li>O caso de uso se encerra.</li>
                </ol>
            </li>
        </ul>
    </div>
</body>
</html>
