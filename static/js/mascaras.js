/**
 * Sistema de Máscaras e Validações para StockBit
 * Aplica máscaras em campos de formulário e valida dados brasileiros
 */

// ============================================================================
// FUNÇÕES DE MÁSCARA
// ============================================================================

/**
 * Aplica máscara de CNPJ (XX.XXX.XXX/XXXX-XX)
 */
function mascaraCNPJ(valor) {
    valor = valor.replace(/\D/g, ''); // Remove tudo que não é dígito
    
    if (valor.length <= 14) {
        valor = valor.replace(/^(\d{2})(\d)/, '$1.$2');
        valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
        valor = valor.replace(/\.(\d{3})(\d)/, '.$1/$2');
        valor = valor.replace(/(\d{4})(\d)/, '$1-$2');
    }
    
    return valor;
}

/**
 * Aplica máscara de CPF (XXX.XXX.XXX-XX)
 */
function mascaraCPF(valor) {
    valor = valor.replace(/\D/g, '');
    
    if (valor.length <= 11) {
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2');
        valor = valor.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    
    return valor;
}

/**
 * Aplica máscara de telefone brasileiro
 * Formato: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
 */
function mascaraTelefone(valor) {
    valor = valor.replace(/\D/g, '');
    
    if (valor.length <= 11) {
        if (valor.length <= 10) {
            // Telefone fixo: (XX) XXXX-XXXX
            valor = valor.replace(/^(\d{2})(\d)/, '($1) $2');
            valor = valor.replace(/(\d{4})(\d)/, '$1-$2');
        } else {
            // Celular: (XX) XXXXX-XXXX
            valor = valor.replace(/^(\d{2})(\d)/, '($1) $2');
            valor = valor.replace(/(\d{5})(\d)/, '$1-$2');
        }
    }
    
    return valor;
}

/**
 * Aplica máscara de CEP (XXXXX-XXX)
 */
function mascaraCEP(valor) {
    valor = valor.replace(/\D/g, '');
    
    if (valor.length <= 8) {
        valor = valor.replace(/^(\d{5})(\d)/, '$1-$2');
    }
    
    return valor;
}

/**
 * Aplica máscara de NCM (XXXXXXXX)
 */
function mascaraNCM(valor) {
    valor = valor.replace(/\D/g, '');
    
    if (valor.length > 8) {
        valor = valor.substring(0, 8);
    }
    
    return valor;
}

/**
 * Aplica máscara de EAN (código de barras - 13 dígitos)
 */
function mascaraEAN(valor) {
    valor = valor.replace(/\D/g, '');
    
    if (valor.length > 13) {
        valor = valor.substring(0, 13);
    }
    
    return valor;
}

// ============================================================================
// FUNÇÕES DE VALIDAÇÃO
// ============================================================================

/**
 * Valida CNPJ usando algoritmo oficial
 */
function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, '');
    
    if (cnpj.length !== 14) {
        return false;
    }
    
    // Elimina CNPJs conhecidos inválidos
    if (/^(\d)\1+$/.test(cnpj)) {
        return false;
    }
    
    // Validação dos dígitos verificadores
    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;
    
    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) {
            pos = 9;
        }
    }
    
    let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0)) {
        return false;
    }
    
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;
    
    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) {
            pos = 9;
        }
    }
    
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1)) {
        return false;
    }
    
    return true;
}

/**
 * Valida CPF usando algoritmo oficial
 */
function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11) {
        return false;
    }
    
    // Elimina CPFs conhecidos inválidos
    if (/^(\d)\1+$/.test(cpf)) {
        return false;
    }
    
    // Validação dos dígitos verificadores
    let soma = 0;
    let resto;
    
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) {
        resto = 0;
    }
    if (resto !== parseInt(cpf.substring(9, 10))) {
        return false;
    }
    
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) {
        resto = 0;
    }
    if (resto !== parseInt(cpf.substring(10, 11))) {
        return false;
    }
    
    return true;
}

/**
 * Valida telefone brasileiro
 */
function validarTelefone(telefone) {
    const numero = telefone.replace(/\D/g, '');
    return numero.length >= 10 && numero.length <= 11;
}

/**
 * Valida CEP brasileiro
 */
function validarCEP(cep) {
    const numero = cep.replace(/\D/g, '');
    return numero.length === 8;
}

/**
 * Valida NCM (8 dígitos)
 */
function validarNCM(ncm) {
    const numero = ncm.replace(/\D/g, '');
    return numero.length === 8;
}

/**
 * Valida EAN (13 dígitos)
 */
function validarEAN(ean) {
    const numero = ean.replace(/\D/g, '');
    return numero.length === 13 || numero.length === 12;
}

// ============================================================================
// INICIALIZAÇÃO
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Aplica máscara de CNPJ
    const camposCNPJ = document.querySelectorAll('input[id*="cnpj"], input[name*="cnpj"], input[id*="CNPJ"], input[name*="CNPJ"]');
    camposCNPJ.forEach(function(campo) {
        campo.addEventListener('input', function(e) {
            const valorAnterior = this.value;
            const novoValor = mascaraCNPJ(e.target.value);
            
            if (novoValor !== valorAnterior) {
                this.value = novoValor;
            }
            
            // Validação em tempo real
            validarCampoCNPJ(this);
        });
        
        campo.addEventListener('blur', function() {
            validarCampoCNPJ(this);
        });
        
        // Aplica máscara no valor inicial se existir
        if (campo.value) {
            campo.value = mascaraCNPJ(campo.value);
        }
    });
    
    // Aplica máscara de Telefone
    const camposTelefone = document.querySelectorAll('input[id*="telefone"], input[name*="telefone"], input[id*="Telefone"], input[name*="Telefone"]');
    camposTelefone.forEach(function(campo) {
        campo.addEventListener('input', function(e) {
            const valorAnterior = this.value;
            const novoValor = mascaraTelefone(e.target.value);
            
            if (novoValor !== valorAnterior) {
                this.value = novoValor;
            }
            
            // Validação em tempo real
            validarCampoTelefone(this);
        });
        
        campo.addEventListener('blur', function() {
            validarCampoTelefone(this);
        });
        
        // Aplica máscara no valor inicial se existir
        if (campo.value) {
            campo.value = mascaraTelefone(campo.value);
        }
    });
    
    // Aplica máscara de CEP
    const camposCEP = document.querySelectorAll('input[id*="cep"], input[name*="cep"], input[id*="CEP"], input[name*="CEP"]');
    camposCEP.forEach(function(campo) {
        campo.addEventListener('input', function(e) {
            this.value = mascaraCEP(e.target.value);
        });
        
        campo.addEventListener('blur', function() {
            if (this.value && !validarCEP(this.value)) {
                mostrarErro(this, 'CEP inválido. Use o formato XXXXX-XXX');
            } else {
                removerErro(this);
            }
        });
        
        // Aplica máscara no valor inicial se existir
        if (campo.value) {
            campo.value = mascaraCEP(campo.value);
        }
    });
    
    // Aplica máscara de NCM
    const camposNCM = document.querySelectorAll('input[id*="ncm"], input[name*="ncm"], input[id*="NCM"], input[name*="NCM"]');
    camposNCM.forEach(function(campo) {
        campo.addEventListener('input', function(e) {
            this.value = mascaraNCM(e.target.value);
        });
        
        campo.addEventListener('blur', function() {
            if (this.value && !validarNCM(this.value)) {
                mostrarErro(this, 'NCM deve ter 8 dígitos');
            } else {
                removerErro(this);
            }
        });
        
        // Aplica máscara no valor inicial se existir
        if (campo.value) {
            campo.value = mascaraNCM(campo.value);
        }
    });
    
    // Aplica máscara de EAN
    const camposEAN = document.querySelectorAll('input[id*="ean"], input[name*="ean"], input[id*="EAN"], input[name*="EAN"]');
    camposEAN.forEach(function(campo) {
        campo.addEventListener('input', function(e) {
            this.value = mascaraEAN(e.target.value);
        });
        
        campo.addEventListener('blur', function() {
            if (this.value && !validarEAN(this.value)) {
                mostrarErro(this, 'EAN deve ter 12 ou 13 dígitos');
            } else {
                removerErro(this);
            }
        });
        
        // Aplica máscara no valor inicial se existir
        if (campo.value) {
            campo.value = mascaraEAN(campo.value);
        }
    });
    
    // Validação melhorada de email
    const camposEmail = document.querySelectorAll('input[type="email"], input[id*="email"], input[name*="email"]');
    camposEmail.forEach(function(campo) {
        campo.addEventListener('blur', function() {
            validarCampoEmail(this);
        });
    });
});

// ============================================================================
// FUNÇÕES AUXILIARES DE VALIDAÇÃO
// ============================================================================

/**
 * Valida e atualiza o estado visual do campo CNPJ
 */
function validarCampoCNPJ(campo) {
    const valor = campo.value.replace(/\D/g, '');
    
    if (!campo.value.trim()) {
        removerErro(campo);
        return;
    }
    
    if (valor.length < 14) {
        mostrarErro(campo, 'CNPJ incompleto');
    } else if (!validarCNPJ(campo.value)) {
        mostrarErro(campo, 'CNPJ inválido');
    } else {
        mostrarSucesso(campo, 'CNPJ válido');
    }
}

/**
 * Valida e atualiza o estado visual do campo Telefone
 */
function validarCampoTelefone(campo) {
    if (!campo.value.trim()) {
        removerErro(campo);
        removerSucesso(campo);
        return;
    }
    
    if (!validarTelefone(campo.value)) {
        mostrarErro(campo, 'Telefone inválido. Use (XX) XXXXX-XXXX ou (XX) XXXX-XXXX');
    } else {
        removerErro(campo);
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
    }
}

/**
 * Valida e atualiza o estado visual do campo Email
 */
function validarCampoEmail(campo) {
    const email = campo.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!email) {
        removerErro(campo);
        removerSucesso(campo);
        return;
    }
    
    if (!emailRegex.test(email)) {
        mostrarErro(campo, 'Email inválido');
    } else {
        mostrarSucesso(campo, 'Email válido');
    }
}

/**
 * Mostra mensagem de erro no campo
 */
function mostrarErro(campo, mensagem) {
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    // Remove mensagem anterior se existir
    removerMensagem(campo);
    
    // Adiciona mensagem de erro
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = mensagem;
    feedback.id = campo.id + '_feedback';
    campo.parentElement.appendChild(feedback);
}

/**
 * Mostra mensagem de sucesso no campo
 */
function mostrarSucesso(campo, mensagem) {
    campo.classList.remove('is-invalid');
    campo.classList.add('is-valid');
    
    // Remove mensagem anterior se existir
    removerMensagem(campo);
    
    // Adiciona mensagem de sucesso (opcional - pode ser removida se não quiser mostrar)
    const feedback = document.createElement('div');
    feedback.className = 'valid-feedback';
    feedback.textContent = mensagem;
    feedback.id = campo.id + '_feedback';
    campo.parentElement.appendChild(feedback);
}

/**
 * Remove mensagem de erro/sucesso
 */
function removerMensagem(campo) {
    const feedback = campo.parentElement.querySelector('#' + campo.id + '_feedback');
    if (feedback) {
        feedback.remove();
    }
}

/**
 * Remove estado de erro
 */
function removerErro(campo) {
    campo.classList.remove('is-invalid');
    removerMensagem(campo);
}

/**
 * Remove estado de sucesso
 */
function removerSucesso(campo) {
    campo.classList.remove('is-valid');
    removerMensagem(campo);
}

