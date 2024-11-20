rule strcpy_rule {
    meta:
        name = "strcpy"
    strings:
        $vuln = "strcpy"
        $notvuln = "strcpy_s"
    condition:
        $vuln and (not $notvuln)
}