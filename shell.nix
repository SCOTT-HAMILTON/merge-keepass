{  }:
let
  pkgs = import <nixpkgs-unstable> {};
  customPython = pkgs.python38.buildEnv.override {
    extraLibs = with pkgs.python38Packages; [
      pykeepass
      click
      pytest
    ];
  };
in
pkgs.mkShell {
  buildInputs = [ customPython ];
  shellHook = ''
    cd ~/GIT/merge-keepass
    run_test(){
      python -c 'import tests;tests.test_merge_databases()'
    }
  '';
}

