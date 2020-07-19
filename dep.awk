{
  printf("%s =", $1);
  for (i = 3; i <= NF; ++i) {
    if ($i ~ /^:/) {
      printf(" %s", $i);
    }
  }
  print "";
}

