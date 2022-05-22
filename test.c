typedef double duplo;
typedef struct al {
  var float nota1, nota2;
} aluno;
var int A, B, C, D;
var duplo E[15];
var aluno F;
function int fatorial(var int a;){
  var int i,result;
  i = 1;
  result =1;
  while (i < a) {
      result =result*i;
      i=i+1;
  }
  return result;
}
function float exp(var float a, b;){
  var int i;
  var float result;
  i = 1;
  result = a;
  if (b == 0) {
    result = 1;
  }
  else {
    while (i < b){
      result = a * a;
      i = i + 1;
    }
  }
  return result;
}
function double maior(var duplo a[15];){
  var int i;
  var double result;
  i = 0;
  result = a[0];
  while (i < 15){
    if (a[i] > result) {
      result = a[i];
      }
    else {
      i = i + 1;
    }
  }
  return result;
}
function aluno lerDados(){
  var aluno result;
  var string msg;
  msg = "digite as notas do aluno";
  printf(msg);
  scanf(result.nota1);
  scanf(result.nota2);
  return result;
}
function int main(){
  A = 10;
  B = fatorial(A);
  C = exp(A,B);
  D = maior(E);
}
