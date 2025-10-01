# Solução para Problemas de Download

## ❌ **Problema: "Nenhum contexto encontrado para exportar"**

### **Causas Possíveis:**
1. **Análise não executada** - Você precisa clicar em "Iniciar Análise" primeiro
2. **Modo muito restritivo** - Modo Estrito pode não encontrar contextos
3. **Texto muito pequeno** - Texto muito curto pode não ter contextos
4. **Backend não funcionando** - API não está respondendo

### **Soluções:**

#### **1. Verificar se a Análise foi Executada**
- ✅ Certifique-se de que clicou em "Iniciar Análise"
- ✅ Aguarde a análise terminar completamente
- ✅ Verifique se aparecem estatísticas (Palavras, Ocorrências, Cantos, Contextos)

#### **2. Usar Modo Completo**
- ✅ Mude de "Modo Estrito" para "Modo Completo"
- ✅ Execute uma nova análise
- ✅ O Modo Completo encontra mais termos relacionados

#### **3. Verificar o Texto**
- ✅ Use um texto maior (pelo menos 1000 palavras)
- ✅ Certifique-se de que o texto contém referências a sonhos
- ✅ Para Os Lusíadas, use o texto completo

#### **4. Verificar Backend**
- ✅ Certifique-se de que o backend está rodando
- ✅ Verifique se a API está respondendo
- ✅ Teste acessando: http://localhost:5000

### **Debug na Interface:**
1. **Após executar a análise**, expanda "🔍 Informações de Debug"
2. **Verifique:**
   - Cantos encontrados: deve ser > 0
   - Contextos por canto: deve mostrar números > 0
   - Tem aggregate: deve ser "Sim"
   - Tem data: deve ser "Sim"

### **Mensagens de Erro Melhoradas:**
- ❌ **Antes:** "Nenhum contexto encontrado para exportar"
- ✅ **Agora:** Mostra estatísticas da análise e dicas para resolver

### **Console do Navegador:**
1. Abra F12 (DevTools)
2. Vá para Console
3. Procure por mensagens de debug
4. Verifique se há erros em vermelho

### **Teste Passo a Passo:**
1. Cole um texto de Os Lusíadas
2. Selecione "Modo Completo"
3. Clique em "Iniciar Análise"
4. Aguarde os resultados
5. Verifique as estatísticas
6. Tente fazer download

### **Se ainda não funcionar:**
1. Verifique o console do navegador
2. Teste com um texto diferente
3. Reinicie o backend
4. Limpe o cache do navegador
