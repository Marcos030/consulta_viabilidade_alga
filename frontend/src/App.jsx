import { useState } from 'react';
import './App.css';
import { consultarViabilidade, uploadPlanilha, limparBase } from './api';

function App() {
  // Estados para Consulta de CEP
  const [cep, setCep] = useState('');
  const [numero, setNumero] = useState('');
  const [resultado, setResultado] = useState(null);
  const [loadingConsulta, setLoadingConsulta] = useState(false);
  const [erroConsulta, setErroConsulta] = useState('');

  // Estados para Upload
  const [arquivoSelecionado, setArquivoSelecionado] = useState(null);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [erroUpload, setErroUpload] = useState('');
  const [sucessoUpload, setSucessoUpload] = useState('');
  const [tempoUpload, setTempoUpload] = useState(0);
  const [intervalId, setIntervalId] = useState(null);

  // Estados para Modal de Confirmação
  const [mostrarModal, setMostrarModal] = useState(false);
  const [loadingLimpar, setLoadingLimpar] = useState(false);

  // Função para aplicar máscara de CEP
  const aplicarMascaraCep = (valor) => {
    // Remove tudo que não é número
    const apenasNumeros = valor.replace(/\D/g, '');

    // Aplica a máscara 00000-000
    if (apenasNumeros.length <= 5) {
      return apenasNumeros;
    }
    return `${apenasNumeros.slice(0, 5)}-${apenasNumeros.slice(5, 8)}`;
  };

  // Handler para o campo CEP
  const handleCepChange = (e) => {
    const valor = e.target.value;
    const valorFormatado = aplicarMascaraCep(valor);
    setCep(valorFormatado);
  };

  // Handler para o campo Número
  const handleNumeroChange = (e) => {
    // Aceita apenas números
    const valor = e.target.value.replace(/\D/g, '');
    setNumero(valor);
  };

  // Validação dos campos
  const isCepValido = () => {
    const apenasNumeros = cep.replace(/\D/g, '');
    return apenasNumeros.length === 8;
  };

  const isNumeroValido = () => {
    return numero.length > 0;
  };

  const isPesquisaHabilitada = () => {
    return isCepValido() && isNumeroValido() && !loadingConsulta;
  };

  // Handler para pesquisar endereço
  const handlePesquisar = async (e) => {
    e.preventDefault();

    if (!isPesquisaHabilitada()) return;

    setLoadingConsulta(true);
    setErroConsulta('');
    setResultado(null);

    try {
      // Remove a máscara do CEP antes de enviar
      const cepSemMascara = cep.replace(/\D/g, '');
      const dados = await consultarViabilidade(cepSemMascara, numero);
      setResultado(dados);

      if (!dados.encontrado) {
        setErroConsulta(dados.mensagem || 'Endereço não encontrado');
      }
    } catch (error) {
      setErroConsulta(error.message || 'Erro ao consultar endereço');
    } finally {
      setLoadingConsulta(false);
    }
  };

  // Handler para seleção de arquivo
  const handleArquivoChange = (e) => {
    const arquivo = e.target.files[0];

    if (!arquivo) {
      setArquivoSelecionado(null);
      setErroUpload('');
      return;
    }

    // Validar extensão
    if (!arquivo.name.endsWith('.xlsx')) {
      setErroUpload('Apenas arquivos .xlsx são aceitos');
      setArquivoSelecionado(null);
      e.target.value = '';
      return;
    }

    // Validar nome do arquivo
    if (arquivo.name !== 'enderecos_nordeste.xlsx') {
      setErroUpload('O arquivo deve se chamar "enderecos_nordeste.xlsx"');
      setArquivoSelecionado(null);
      e.target.value = '';
      return;
    }

    setArquivoSelecionado(arquivo);
    setErroUpload('');
    setSucessoUpload('');
  };

  // Iniciar timer
  const iniciarTimer = () => {
    setTempoUpload(0);
    const id = setInterval(() => {
      setTempoUpload((prev) => prev + 1);
    }, 1000);
    setIntervalId(id);
  };

  // Parar timer
  const pararTimer = () => {
    if (intervalId) {
      clearInterval(intervalId);
      setIntervalId(null);
    }
  };

  // Formatar tempo em MM:SS
  const formatarTempo = (segundos) => {
    const minutos = Math.floor(segundos / 60);
    const segs = segundos % 60;
    return `${String(minutos).padStart(2, '0')}:${String(segs).padStart(2, '0')}`;
  };

  // Handler para upload de planilha
  const handleUpload = async (e) => {
    e.preventDefault();

    if (!arquivoSelecionado) {
      setErroUpload('Selecione um arquivo primeiro');
      return;
    }

    setLoadingUpload(true);
    setErroUpload('');
    setSucessoUpload('');
    iniciarTimer();

    try {
      const dados = await uploadPlanilha(arquivoSelecionado);
      setSucessoUpload(dados.mensagem || 'Upload realizado com sucesso!');
      setArquivoSelecionado(null);
      // Limpar o input file
      document.getElementById('file-upload').value = '';
    } catch (error) {
      setErroUpload(error.message || 'Erro ao fazer upload');
    } finally {
      setLoadingUpload(false);
      pararTimer();
    }
  };

  // Handler para limpar base de dados
  const handleLimparBase = async () => {
    setLoadingLimpar(true);

    try {
      await limparBase();
      setMostrarModal(false);
      alert('Base de dados limpa com sucesso!');
      // Limpar resultados da consulta
      setResultado(null);
    } catch (error) {
      alert(error.message || 'Erro ao limpar base de dados');
    } finally {
      setLoadingLimpar(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Sistema de Consulta de Viabilidade de Endereços</h1>
        <p>Nordeste do Brasil - Alga</p>
      </header>

      <main className="main-content">
        {/* Seção 1: Consulta de CEP */}
        <section className="secao-consulta">
          <h2>Consultar Endereço</h2>

          <form onSubmit={handlePesquisar} className="form-consulta">
            <div className="form-group">
              <label htmlFor="cep">CEP *</label>
              <input
                type="text"
                id="cep"
                value={cep}
                onChange={handleCepChange}
                placeholder="00000-000"
                maxLength={9}
                className={cep && !isCepValido() ? 'input-erro' : ''}
                required
              />
              {cep && !isCepValido() && (
                <span className="erro-campo">CEP deve ter 8 dígitos</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="numero">Número *</label>
              <input
                type="text"
                id="numero"
                value={numero}
                onChange={handleNumeroChange}
                placeholder="Ex: 144"
                className={numero && !isNumeroValido() ? 'input-erro' : ''}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={!isPesquisaHabilitada()}
            >
              {loadingConsulta ? 'Pesquisando...' : 'Pesquisar'}
            </button>
          </form>

          {erroConsulta && (
            <div className="mensagem erro">
              {erroConsulta}
            </div>
          )}

          {resultado && resultado.encontrado && (
            <div className="resultado">
              <h3>Resultado da Consulta</h3>
              <table className="tabela-resultado">
                <thead>
                  <tr>
                    <th>Viabilidade</th>
                    <th>Município</th>
                    <th>Bairro</th>
                    <th>Logradouro</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className={resultado.detalhes?.viabilidade_atual === 'Viável' ? 'viavel' : 'nao-viavel'}>
                      {resultado.detalhes?.viabilidade_atual || resultado.viabilidade || '-'}
                    </td>
                    <td>{resultado.detalhes?.municipio || '-'}</td>
                    <td>{resultado.detalhes?.bairro || '-'}</td>
                    <td>{resultado.detalhes?.logradouro || '-'}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Seção 2 e 3: Upload e Limpar */}
        <aside className="secao-lateral">
          {/* Seção 2: Upload de Planilha */}
          <section className="secao-upload">
            <h2>Upload de Planilha</h2>

            <form onSubmit={handleUpload} className="form-upload">
              <div className="form-group">
                <label htmlFor="file-upload" className="label-file">
                  Selecionar Arquivo
                </label>
                <input
                  type="file"
                  id="file-upload"
                  accept=".xlsx"
                  onChange={handleArquivoChange}
                  disabled={loadingUpload}
                />
                {arquivoSelecionado && (
                  <span className="nome-arquivo">{arquivoSelecionado.name}</span>
                )}
                <small className="dica">
                  Aceita apenas: <strong>enderecos_nordeste.xlsx</strong>
                </small>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={!arquivoSelecionado || loadingUpload}
              >
                {loadingUpload ? 'Enviando...' : 'Enviar Planilha'}
              </button>
            </form>

            {loadingUpload && (
              <div className="upload-progress">
                <div className="timer">
                  Tempo decorrido: <strong>{formatarTempo(tempoUpload)}</strong>
                </div>
                <div className="progress-bar">
                  <div className="progress-bar-fill"></div>
                </div>
                <p className="texto-progresso">
                  Processando... isso pode levar até 9 minutos
                </p>
              </div>
            )}

            {erroUpload && (
              <div className="mensagem erro">{erroUpload}</div>
            )}

            {sucessoUpload && (
              <div className="mensagem sucesso">{sucessoUpload}</div>
            )}
          </section>

          {/* Seção 3: Limpar Base */}
          <section className="secao-limpar">
            <h2>Gerenciar Dados</h2>
            <p className="descricao-limpar">
              Remove todos os dados do banco de dados.
            </p>
            <button
              className="btn btn-danger"
              onClick={() => setMostrarModal(true)}
            >
              Limpar Base de Dados
            </button>
          </section>
        </aside>
      </main>

      {/* Modal de Confirmação */}
      {mostrarModal && (
        <div className="modal-overlay" onClick={() => setMostrarModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Confirmar Exclusão</h3>
            <p>
              Tem certeza que deseja limpar a base de dados?
              <br />
              <strong>Esta ação não pode ser desfeita!</strong>
            </p>
            <div className="modal-buttons">
              <button
                className="btn btn-secondary"
                onClick={() => setMostrarModal(false)}
                disabled={loadingLimpar}
              >
                Cancelar
              </button>
              <button
                className="btn btn-danger"
                onClick={handleLimparBase}
                disabled={loadingLimpar}
              >
                {loadingLimpar ? 'Limpando...' : 'Sim, Limpar'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
