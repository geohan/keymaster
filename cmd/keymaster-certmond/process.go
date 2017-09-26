package main

import (
	"bytes"
	"crypto/x509"
	"golang.org/x/crypto/ssh"
	"os"
	"os/exec"
)

func (c certCommand) processX509Cert(cert *x509.Certificate) error {
	args := make([]string, 0, len(c.Parameters))
	for _, template := range c.templates {
		buffer := &bytes.Buffer{}
		if err := template.Execute(buffer, cert); err != nil {
			return err
		}
		args = append(args, buffer.String())
	}
	cmd := exec.Command(c.Command, args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func (c certCommand) processSshCert(cert *ssh.Certificate) error {
	args := make([]string, 0, len(c.Parameters))
	for _, template := range c.templates {
		buffer := &bytes.Buffer{}
		if err := template.Execute(buffer, cert); err != nil {
			return err
		}
		args = append(args, buffer.String())
	}
	cmd := exec.Command(c.Command, args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func processRawCert(command string, cert []byte) error {
	cmd := exec.Command(command)
	cmd.Stdin = bytes.NewBuffer(cert)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}
