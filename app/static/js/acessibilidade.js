// Barra de acessibilidade: alto contraste e fonte ampliada.
// A preferência fica salva no navegador do voluntário (localStorage).
(function () {
  var raiz = document.documentElement;
  var opcoes = { contraste: "alto-contraste", fonte: "fonte-grande" };

  function lerPreferencia(chave) {
    try { return localStorage.getItem("a11y-" + chave) === "1"; } catch (e) { return false; }
  }

  function salvarPreferencia(chave, ativo) {
    try { localStorage.setItem("a11y-" + chave, ativo ? "1" : "0"); } catch (e) { /* sem armazenamento */ }
  }

  function aplicar(chave, ativo) {
    raiz.classList.toggle(opcoes[chave], ativo);
    var botao = document.querySelector('[data-a11y="' + chave + '"]');
    if (botao) botao.setAttribute("aria-pressed", ativo ? "true" : "false");
  }

  document.addEventListener("DOMContentLoaded", function () {
    Object.keys(opcoes).forEach(function (chave) {
      aplicar(chave, lerPreferencia(chave));
      var botao = document.querySelector('[data-a11y="' + chave + '"]');
      if (!botao) return;
      botao.addEventListener("click", function () {
        var ativo = botao.getAttribute("aria-pressed") !== "true";
        aplicar(chave, ativo);
        salvarPreferencia(chave, ativo);
      });
    });
  });
})();
